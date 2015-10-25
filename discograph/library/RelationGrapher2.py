# -*- encoding: utf-8 -*-
import collections
import itertools
import math
import re
import six
from discograph.library.CreditRole import CreditRole
from discograph.library.TrellisNode2 import TrellisNode2
from discograph.library.postgres.PostgresEntity import PostgresEntity
from discograph.library.postgres.PostgresRelation import PostgresRelation


class RelationGrapher2(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_break_on_next_loop',
        '_center_entity',
        '_degree',
        '_entity_keys_to_visit',
        '_link_ratio',
        '_links',
        '_max_nodes',
        '_nodes',
        '_relational_roles',
        '_structural_roles',
        )

    roles_to_prune = [
        'Released On',
        'Compiled On',
        'Producer',
        'Remix',
        'DJ Mix',
        'Written-By',
        ]

    word_pattern = re.compile('\s+')

    ### INITIALIZER ###

    def __init__(
        self,
        center_entity,
        degree=3,
        link_ratio=None,
        max_nodes=None,
        roles=None,
        ):
        assert isinstance(center_entity, PostgresEntity)
        self._center_entity = center_entity
        degree = int(degree)
        assert 0 < degree
        self._degree = degree
        if max_nodes is not None:
            max_nodes = int(max_nodes)
            assert 0 < max_nodes
        else:
            max_nodes = 100
        self._max_nodes = max_nodes
        if link_ratio is not None:
            link_ratio = int(link_ratio)
            assert 0 < link_ratio
        else:
            link_ratio = 3
        self._link_ratio = link_ratio
        roles = roles or ()
        structural_roles, relational_roles = [], []
        if roles:
            if isinstance(roles, six.string_types):
                roles = (roles,)
            elif not isinstance(roles, collections.Iterable):
                roles = (roles,)
            roles = tuple(roles)
            assert all(_ in CreditRole.all_credit_roles for _ in roles)
            for role in roles:
                if role in ('Alias', 'Sublabel Of', 'Member Of'):
                    structural_roles.append(role)
                else:
                    relational_roles.append(role)
        self._structural_roles = tuple(structural_roles)
        self._relational_roles = tuple(relational_roles)
        self._nodes = collections.OrderedDict()
        self._links = {}
        self._break_on_next_loop = False
        self._entity_keys_to_visit = set()

    ### SPECIAL METHODS ###

    def __call__(self):
        provisional_roles = list(self.relational_roles)
        self._report_search_start()
        self._clear()
        self.entity_keys_to_visit.add(self.center_entity.entity_key)
        for distance in range(self.degree + 1):
            self._report_search_loop_start(distance)
            print('        Retrieving entities')
            entities = PostgresEntity.search_multi(self.entity_keys_to_visit)
            relations = {}
            self._process_entities(distance, entities)
            if self.break_on_next_loop:
                print('        Exiting search loop.')
                break
            self._test_loop_one(distance)
            self._prune_roles(distance, provisional_roles)
            self._search_via_structural_roles(distance, provisional_roles, relations)
            self._search_via_relational_roles(distance, provisional_roles, relations)
            self._test_loop_two(distance, relations)
            self.entity_keys_to_visit.clear()
            self._process_relations(relations)
        self._cross_reference()
        self._build_trellis()
        pages = self._partition_trellis()
        self._page_entities(pages)
        for node in self.nodes.values():
            expected_count = node.entity.roles_to_relation_count(self.all_roles)
            node.missing = expected_count - len(node.links)
        json_links = tuple(link.as_json() for key, link in
            sorted(self.links.items(), key=lambda x: x[0]))
        json_nodes = tuple(node.as_json() for key, node in
            sorted(self.nodes.items(), key=lambda x: x[0]))
        network = {
            'center': {
                'key': self.center_entity.json_entity_key,
                'name': self.center_entity.name,
                },
            'links': json_links,
            'nodes': json_nodes,
            'pages': len(pages),
            }
        return network

    ### PRIVATE METHODS ###

    def _page_entities(self, pages):
        for page_number, page in enumerate(pages, 1):
            for node in page:
                node.pages.add(page_number)
        grouped_links = {}
        for link in self.links.values():
            key = tuple(sorted([link.entity_one_key, link.entity_two_key]))
            grouped_links.setdefault(key, [])
            grouped_links[key].append(link)
        for (e1k, e2k), links in grouped_links.items():
            entity_one_pages = self.nodes[e1k].pages
            entity_two_pages = self.nodes[e2k].pages
            intersection = entity_one_pages.intersection(entity_two_pages)
            for link in links:
                link.pages = intersection
        for node in self.nodes.values():
            node.missing_by_page.update({page_number: 0 for page_number in node.pages})
            neighbors = node.get_neighbors()
            for neighbor in neighbors:
                for page_number in node.pages.difference(neighbor.pages):
                    node.missing_by_page[page_number] += 1
            if not any(node.missing_by_page.values()):
                node.missing_by_page.clear()

    def _group_trellis(self, trellis):
        trellis_nodes_by_distance = collections.OrderedDict()
        for trellis_node in trellis.values():
            if trellis_node.distance not in trellis_nodes_by_distance:
                trellis_nodes_by_distance[trellis_node.distance] = set()
            trellis_nodes_by_distance[trellis_node.distance].add(trellis_node)
        return trellis_nodes_by_distance

    def _build_trellis(self):
        for link_key, relation in tuple(self.links.items()):
            if (
                relation.entity_one_key not in self.nodes or
                relation.entity_two_key not in self.nodes
                ):
                self.links.pop(link_key)
                continue
            source_node = self.nodes[relation.entity_one_key]
            source_node.links.add(link_key)
            target_node = self.nodes[relation.entity_two_key]
            target_node.links.add(link_key)
            if source_node.distance == target_node.distance:
                source_node.siblings.add(target_node)
                target_node.siblings.add(source_node)
            elif source_node.distance < target_node.distance:
                source_node.children.add(target_node)
                target_node.parents.add(source_node)
            elif target_node.distance < source_node.distance:
                target_node.children.add(source_node)
                source_node.parents.add(target_node)
        self._recurse_trellis(self.nodes[self.center_entity.entity_key])

    def _partition_trellis(self):
        print('    Partitioning trellis...')
        message = '        Maximum: {} / {}'
        message = message.format(self.max_nodes, self.max_links)
        print(message)
        page_count = math.ceil(float(len(self.nodes)) / self.max_nodes)
        pages = [set() for _ in range(page_count)]
        trellis_nodes_by_distance = self._group_trellis(self.nodes)
        threshold = len(self.nodes) / len(pages) / len(trellis_nodes_by_distance)
        winning_distance = self._find_trellis_distance(
            trellis_nodes_by_distance,
            threshold,
            )
        self._page_by_local_neighborhood(pages, trellis_nodes_by_distance)
        self._page_at_winning_distance(pages, trellis_nodes_by_distance, winning_distance)
        self._page_by_distance(pages, trellis_nodes_by_distance)
        for i, page in enumerate(pages):
            message = '        Page {}: {}'
            message = message.format(i, len(page))
            print(message)
        return pages

    def _page_at_winning_distance(
        self,
        pages,
        trellis_nodes_by_distance,
        winning_distance,
        ):
        while trellis_nodes_by_distance[winning_distance]:
            trellis_node = trellis_nodes_by_distance[winning_distance].pop(0)
            parentage = trellis_node.get_parentage()
            pages.sort(
                key=lambda page: (
                    len(page.difference(parentage)),
                    len(page),
                    ),
                )
            pages[0].update(parentage)

    def _page_by_local_neighborhood(
        self,
        pages,
        trellis_nodes_by_distance,
        verbose=True,
        ):
        local_neighborhood = []
        neighborhood_threshold = (len(self.nodes) / len(pages))
        for distance, trellis_nodes in sorted(trellis_nodes_by_distance.items()):
            if len(local_neighborhood) + len(trellis_nodes) < neighborhood_threshold:
                local_neighborhood.extend(trellis_nodes)
                trellis_nodes[:] = []
        message = '        Local neighborhood: {}'
        message = message.format(len(local_neighborhood))
        print(message)
        for trellis_node in local_neighborhood:
            parentage = trellis_node.get_parentage()
            for page in pages:
                page.update(parentage)

    def _page_by_distance(
        self,
        pages,
        trellis_nodes_by_distance,
        ):
        for distance in sorted(trellis_nodes_by_distance):
            while trellis_nodes_by_distance[distance]:
                trellis_node = trellis_nodes_by_distance[distance].pop(0)
                parentage = trellis_node.get_parentage()
                pages.sort(
                    key=lambda page: (
                        len(page.difference(parentage)),
                        len(page),
                        ),
                    )
                pages[0].update(parentage)

    def _find_trellis_distance(
        self,
        trellis_nodes_by_distance,
        threshold,
        verbose=True,
        ):
        if verbose:
            message = '        Maximum depth: {}'
            message = message.format(max(trellis_nodes_by_distance))
            print(message)
            message = '        Subgraph threshold: {}'
            message = message.format(threshold)
            print(message)
        distancewise_average_subgraph_size = {}
        for distance, trellis_nodes in trellis_nodes_by_distance.items():
            trellis_nodes_by_distance[distance] = sorted(
                trellis_nodes,
                key=lambda x: x.entity_key,
                )
            sizes = sorted(_.subgraph_size for _ in trellis_nodes)
            geometric = sum(sizes) ** (1.0 / len(sizes))
            distancewise_average_subgraph_size[distance] = geometric
            if verbose:
                message = '            At distance {}: {} geometric mean'
                message = message.format(distance, geometric)
                print(message)
        winning_distance = 0
        pairs = ((a, d) for d, a in distancewise_average_subgraph_size.items())
        pairs = sorted(pairs, reverse=True)
        for average, distance in pairs:
            if verbose:
                message = '                Testing {} @ distance {}'
                message = message.format(average, distance)
                print(message)
            if average < threshold:
                winning_distance = distance
                break
        if verbose:
            message = '            Winning distance: {}'
            message = message.format(winning_distance)
            print(message)
        if (winning_distance + 1) < (len(distancewise_average_subgraph_size) / 2):
            winning_distance += 1
            if verbose:
                message = '            Promoting winning distance: {}'
                message = message.format(winning_distance)
                print(message)
        return winning_distance

    def _clear(self):
        self._nodes.clear()
        self._links.clear()
        self._entity_keys_to_visit.clear()
        self._break_on_next_loop = False

    def _cross_reference(self):
        relations = {}
        entity_keys = sorted(self.nodes)
        entity_keys.remove(self.center_entity.entity_key)
        entity_key_slices = []
        step = 1000
        for start in range(0, len(entity_keys), step):
            entity_key_slices.append(entity_keys[start:start + step])
        iterator = itertools.product(entity_key_slices, entity_key_slices)
        for lh_entities, rh_entities in iterator:
            found = PostgresRelation.search_bimulti(
                lh_entities,
                rh_entities,
                roles=self.relational_roles,
                )
            relations.update(found)
        self._process_relations(relations)
        message = '    Cross-referenced: {} / {}'
        message = message.format(len(self.nodes), len(self.links))
        print(message)

    def _prune_roles(self, distance, provisional_roles):
        if 0 < distance and self.max_nodes / 4 < len(self.nodes):
            for role in self.roles_to_prune:
                if role in provisional_roles:
                    print('            Pruned {!r} role'.format(role))
                    provisional_roles.remove(role)
            if self.center_entity.entity_type == 1:
                if 'Sublabel Of' in provisional_roles:
                    print('            Pruned {!r} role'.format('Sublabel Of'))
                    provisional_roles.remove('Sublabel Of')

    def _process_entities(self, distance, entities):
        for entity in entities:
            if not all([
                entity.entity_id,
                entity.name,
                ]):
                self.entity_keys_to_visit.remove(entity.entity_key)
                continue
            entity_key = entity.entity_key
            if entity_key not in self.nodes:
                self.nodes[entity_key] = TrellisNode2(entity, distance)

    def _process_relations(self, relations):
        for link_key, relation in relations.items():
            if not relation.entity_one_id or not relation.entity_two_id:
                continue
            entity_one_key = relation.entity_one_key
            entity_two_key = relation.entity_two_key
            if entity_one_key not in self.nodes:
                self.entity_keys_to_visit.add(entity_one_key)
            if entity_two_key not in self.nodes:
                self.entity_keys_to_visit.add(entity_two_key)
            self.links[link_key] = relation

    def _recurse_trellis(self, node):
        traversed_keys = set([node.entity_key])
        for child in node.children:
            traversed_keys.update(self._recurse_trellis(child))
        node.subgraph_size = len(traversed_keys)
        #print('{}{}: {}'.format('    ' * node.distance, node.entity.name, node.subgraph_size))
        return traversed_keys

    def _report_search_loop_start(
        self,
        distance,
        ):
        to_visit_count = len(self.entity_keys_to_visit)
        message = '    At distance {}:'
        message = message.format(distance)
        print(message)
        message = '        {} old nodes'
        message = message.format(len(self.nodes))
        print(message)
        message = '        {} old links'
        message = message.format(len(self.links))
        print(message)
        message = '        {} new nodes'
        message = message.format(to_visit_count)
        print(message)

    def _report_search_start(self):
        message = '    Max nodes: {}'
        message = message.format(self.max_nodes)
        print(message)
        message = '    Max links: {}'
        message = message.format(self.max_links)
        print(message)
        message = '    Roles: {}'
        message = message.format(self.all_roles)
        print(message)

    def _search_via_structural_roles(self, distance, provisional_roles, relations):
        if not self.structural_roles:
            return
        print('        Retrieving structural relations')
        for entity_key in sorted(self.entity_keys_to_visit):
            node = self.nodes.get(entity_key)
            if not node:
                continue
            entity = node.entity
            relations.update(entity.structural_roles_to_relations(self.structural_roles))

    def _search_via_relational_roles(self, distance, provisional_roles, relations):
        for entity_key in sorted(self.entity_keys_to_visit):
            node = self.nodes.get(entity_key)
            if not node:
                continue
            entity = node.entity
            relational_count = entity.roles_to_relation_count(provisional_roles)
            if 0 < distance and self.max_links < relational_count:
                self.entity_keys_to_visit.remove(entity_key)
                message = '            Pre-pruned {} [{}]'
                message = message.format(entity.name, relational_count)
                print(message)
        if provisional_roles and distance < self.degree:
            print('        Retrieving relational relations')
            keys = sorted(self.entity_keys_to_visit)
            for start in range(0, len(keys), 500):
                key_slice = keys[start:start + 500]
                print('            {}-{} of {}'.format(start, start + 500, len(keys)))
                relations.update(
                    PostgresRelation.search_multi(
                        key_slice,
                        roles=provisional_roles,
                        )
                    )

    def _test_loop_one(self, distance):
        if 0 < distance:
            if self.max_nodes <= len(self.nodes):
                print('        Max nodes: exiting next search loop.')
                self.break_on_next_loop = True

    def _test_loop_two(self, distance, relations):
        if not relations:
            self.break_on_next_loop = True
        if self.max_links * 3 <= len(relations):
            print('        Max links: exiting next search loop.')
            self.break_on_next_loop = True
        if 1 < distance:
            if self.max_links <= len(relations):
                print('        Max links: exiting next search loop.')
                self.break_on_next_loop = True

    ### PUBLIC PROPERTIES ###

    @property
    def all_roles(self):
        return self.structural_roles + self.relational_roles

    @property
    def break_on_next_loop(self):
        return self._break_on_next_loop

    @break_on_next_loop.setter
    def break_on_next_loop(self, expr):
        self._break_on_next_loop = bool(expr)

    @property
    def center_entity(self):
        return self._center_entity

    @property
    def degree(self):
        return self._degree

    @property
    def entity_keys_to_visit(self):
        return self._entity_keys_to_visit

    @property
    def link_ratio(self):
        return self._link_ratio

    @property
    def links(self):
        return self._links

    @property
    def max_links(self):
        return self._max_nodes * self._link_ratio

    @property
    def max_nodes(self):
        return self._max_nodes

    @property
    def nodes(self):
        return self._nodes

    @property
    def relational_roles(self):
        return self._relational_roles

    @property
    def structural_roles(self):
        return self._structural_roles