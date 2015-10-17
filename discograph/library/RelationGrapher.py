# -*- encoding: utf-8 -*-
import collections
import itertools
import math
import re
import redis
import six
from discograph.library.TrellisNode import TrellisNode
from discograph.library.CreditRole import CreditRole
from discograph.library.sqlite.SqliteEntity import SqliteEntity
from discograph.library.sqlite.SqliteRelation import SqliteRelation


class RelationGrapher(object):

    ### CLASS VARIABLES ###

    core_roles = [
        'Alias',
        'Member Of',
        'Released On',
        'Sublabel Of',
        ]

    entity_type_names = {
        1: 'artist',
        2: 'label',
        }

    entity_name_types = {
        'artist': 1,
        'label': 2,
        }

    roles_to_prune = [
        'Released On',
        'Compiled On',
        'Producer',
        'Remix',
        'DJ Mix',
        'Written-By',
        ]

    word_pattern = re.compile('\s+')

    redis_client = redis.StrictRedis()

    ### INITIALIZER ###

    def __init__(
        self,
        center_entity,
        degree=3,
        link_ratio=None,
        max_nodes=None,
        roles=None,
        year=None,
        ):
        assert isinstance(center_entity, SqliteEntity)
        self.center_entity = center_entity
        degree = int(degree)
        assert 0 < degree
        self.degree = degree
        if max_nodes is not None:
            max_nodes = int(max_nodes)
            assert 0 < max_nodes
        else:
            max_nodes = 100
        self.max_nodes = max_nodes
        if link_ratio is not None:
            link_ratio = int(link_ratio)
            assert 0 < link_ratio
        else:
            link_ratio = 3
        self.link_ratio = link_ratio
        roles = roles or None
        if roles:
            if isinstance(roles, six.string_types):
                roles = (roles,)
            elif not isinstance(roles, collections.Iterable):
                roles = (roles,)
            roles = tuple(roles)
            assert all(_ in CreditRole.all_credit_roles
                for _ in roles)
        self.roles = roles
        if year is not None:
            if isinstance(year, collections.Sequence):
                year = tuple(int(_) for _ in year)
                assert len(year) == 2
            else:
                year = int(year)
        self.year = year

    def build_trellis(self, nodes, links, verbose=True):
        def recurse_trellis(node):
            subgraph_size = 1
            for child in node.children:
                if child.subgraph_size is None:
                    recurse_trellis(child)
                subgraph_size += child.subgraph_size
            node.subgraph_size = subgraph_size
        if verbose:
            message = '    Building trellis...'
            print(message)
        trellis = collections.OrderedDict()
        nodes = sorted(nodes.values(), key=lambda x: (x['distance'], x['id']))
        for node in nodes:
            if node['type'] == 'artist':
                node_type = 1
            elif node['type'] == 'label':
                node_type = 2
            else:
                raise ValueError(node)
            key = (node_type, node['id'])
            trellis[key] = TrellisNode(node)
        for link in links.values():
            node_one = trellis.get(link['source'])
            node_two = trellis.get(link['target'])
            if node_one is None or node_two is None:
                continue
            if node_one.distance == node_two.distance:
                node_one.siblings.add(node_two)
                node_two.siblings.add(node_one)
            elif node_one.distance < node_two.distance:
                node_one.children.add(node_two)
                node_two.parents.add(node_one)
            else:
                node_two.children.add(node_one)
                node_one.parents.add(node_two)
        root_key = (
            self.center_entity.entity_type,
            self.center_entity.entity_id,
            )
        recurse_trellis(trellis[root_key])
        assert len(trellis) == len(nodes)
        return trellis

    def collect_entities(self, verbose=True):
        original_roles = self.roles or ()
        provisional_roles = set(original_roles)
        provisional_roles.update(['Alias', 'Member Of'])
        provisional_roles = sorted(provisional_roles)
        initial_key = (
            self.center_entity.entity_type,
            self.center_entity.entity_id,
            )
        entity_keys_to_visit = set([initial_key])
        links = dict()
        nodes = dict()
        break_on_next_loop = False
        max_nodes = self.max_nodes or 100
        max_links = self.link_ratio * max_nodes
        self.report_search_start(
            max_links,
            max_nodes,
            original_roles,
            verbose=verbose,
            )

        ###

        for distance in range(self.degree + 1):
            to_visit = list(entity_keys_to_visit)
            for key in to_visit:
                nodes.setdefault(key, self.entity_key_to_node(key, distance))

            ###

            self.report_search_loop_start(
                distance,
                links,
                nodes,
                to_visit,
                verbose=verbose,
                )
            if break_on_next_loop:
                if verbose:
                    print('        Exiting search loop.')
                break
            if 0 < distance and max_nodes / 4 < len(nodes):
                for role in self.roles_to_prune:
                    if role in provisional_roles:
                        provisional_roles.remove(role)
                if self.center_entity.entity_type == 1:
                    if 'Sublabel Of' in provisional_roles:
                        provisional_roles.remove('Sublabel Of')
            if 0 < distance:
                if max_nodes <= len(nodes):
                    if verbose:
                        print('        Max nodes: exiting next search loop.')
                    break_on_next_loop = True

            ###

            relations = self.query_relations(
                entity_keys=to_visit,
                distance=distance,
                nodes=nodes,
                links=links,
                roles=provisional_roles,
                year=None,
                verbose=verbose,
                )

            ###

            if verbose:
                message = '            {} new links'
                message = message.format(len(relations))
                print(message)
            if not relations:
                break
            if 1 < distance:
                if max_links * 3 <= len(relations):
                    if verbose: print('        Max links: exiting immediately.')
                    break
                if max_links <= len(relations):
                    if verbose: print('        Max links: exiting next search loop.')
                    break_on_next_loop = True

            ###

            entity_keys_to_visit.clear()
            for relation in relations:
                self.process_relation(
                    distance=distance,
                    entity_keys_to_visit=entity_keys_to_visit,
                    links=links,
                    nodes=nodes,
                    original_roles=original_roles,
                    relation=relation,
                    )

        ###

        if 'Released On' in original_roles:
            relations = self.cross_reference(nodes, roles=['Released On'])
            relations = self.group_relations_for_collection(relations)
            for relation in relations:
                self.process_relation(
                    distance=distance,
                    entity_keys_to_visit=entity_keys_to_visit,
                    links=links,
                    nodes=nodes,
                    original_roles=original_roles,
                    relation=relation,
                    )

        ###

        if verbose:
            message = '    Collected: {} / {}'
            message = message.format(len(nodes), len(links))
            print(message)

        ###

        self.query_node_names(nodes)
        self.prune_nameless(nodes, links, verbose=verbose)
        self.prune_not_on_label(nodes, links, verbose=verbose)
        self.prune_unvisited(entity_keys_to_visit, nodes, links, verbose=verbose)
        trellis = self.build_trellis(nodes, links, verbose=verbose)
        pages = self.partition_trellis(trellis, nodes, links)
        self.page_entities(nodes, links, pages, trellis)
        self.prune_unpaged_links(nodes, links, verbose=verbose)

        ###

        if verbose:
            print('Finally: {} / {}'.format(len(nodes), len(links)))
        return nodes, links

    def entity_key_to_node(self, entity_key, distance):
        node = dict(distance=distance, missing=0, members=set(), aliases=set())
        node['id'] = entity_key[1]
        if entity_key[0] == 1:
            node['type'] = 'artist'
        else:
            node['type'] = 'label'
        node['key'] = '{}-{}'.format(node['type'], node['id'])
        node['links'] = set()
        return node

    def group_trellis(self, trellis):
        trellis_nodes_by_distance = collections.OrderedDict()
        for trellis_node in trellis.values():
            if trellis_node.distance not in trellis_nodes_by_distance:
                trellis_nodes_by_distance[trellis_node.distance] = set()
            trellis_nodes_by_distance[trellis_node.distance].add(trellis_node)
        return trellis_nodes_by_distance

    def page_at_winning_distance(
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

    def page_by_local_neighborhood(
        self,
        pages,
        trellis,
        trellis_nodes_by_distance,
        verbose=True,
        ):
        local_neighborhood = []
        neighborhood_threshold = (len(trellis) / len(pages))
        for distance, trellis_nodes in sorted(trellis_nodes_by_distance.items()):
            if len(local_neighborhood) + len(trellis_nodes) < neighborhood_threshold:
                local_neighborhood.extend(trellis_nodes)
                trellis_nodes[:] = []
        if verbose:
            message = '        Local neighborhood: {}'
            message = message.format(len(local_neighborhood))
            print(message)
        for trellis_node in local_neighborhood:
            parentage = trellis_node.get_parentage()
            for page in pages:
                page.update(parentage)

    def page_by_distance(
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

    def find_trellis_distance(
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

    @classmethod
    def get_link_key(cls, link):
        source_type, source_id = link['source']
        if source_type == 1:
            source_type = 'artist'
        else:
            source_type = 'label'
        target_type, target_id = link['target']
        if target_type == 1:
            target_type = 'artist'
        else:
            target_type = 'label'
        pieces = [
            source_type,
            source_id,
            cls.word_pattern.sub('-', link['role']).lower(),
            target_type,
            target_id,
            ]
        return '-'.join(str(_) for _ in pieces)

    def get_network(self):
        nodes, links = self.collect_entities()
        nodes = self.postprocess_nodes(nodes)
        links = self.postprocess_links(links)
        if self.center_entity.entity_type == 1:
            key = 'artist-{}'.format(self.center_entity.entity_id)
        elif self.center_entity.entity_type == 2:
            key = 'label-{}'.format(self.center_entity.entity_id)
        else:
            raise ValueError(self.center_entity)
        pages = set()
        for node in nodes:
            pages.update(node['pages'])
        pages = len(pages)
        network = {
            'center': {
                'key': key,
                'name': self.center_entity.name,
                },
            'links': links,
            'nodes': nodes,
            'pages': pages,
            }
        return network

    def group_relations_for_collection(self, relations):
        grouped_links = {}
        for relation in relations:
            e1k = (relation.entity_one_type, relation.entity_one_id)
            e2k = (relation.entity_two_type, relation.entity_two_id)
            link = dict(
                role=relation.role,
                source=e1k,
                target=e2k,
                )
            key = link['key'] = self.get_link_key(link)
            if key not in grouped_links:
                grouped_links[key] = link
            if relation.release_id != -1:
                if 'releases' not in grouped_links[key]:
                    grouped_links[key]['releases'] = {}
                grouped_links[key]['releases'][relation.release_id] = relation.year
        return list(grouped_links.values())

    def group_links_for_paging(self, links):
        grouped_links = {}
        for link in links.values():
            key = tuple(sorted([link['source'], link['target']]))
            grouped_links.setdefault(key, [])
            grouped_links[key].append(link)
        return grouped_links

    @staticmethod
    def link_sorter(link):
        role = 2
        if link['role'] == 'Alias':
            role = 0
        elif link['role'] == 'Member Of':
            role = 1
        return link['distance'], role, link['key']

    def page_entities(self, nodes, links, pages, trellis):
        for page_number, page in enumerate(pages, 1):
            for trellis_node in page:
                node = trellis_node.node
                node.setdefault('pages', set())
                node['pages'].add(page_number)
        # links whose nodes do not share any pages should be pruned
        for (e1k, e2k), grouped_links in self.group_links_for_paging(links).items():
            entity_one_pages = nodes[e1k]['pages']
            entity_two_pages = nodes[e2k]['pages']
            intersection = entity_one_pages.intersection(entity_two_pages)
            for link in grouped_links:
                link['pages'] = intersection
        # also pre-calculate, for each node, how many neighbors are missing per page
        # e.g. [0, 5, 2] -> {1: 0, 2: 5, 3: 2} missing entities
        # this will simplify front-end paging logic
        for trellis_node in trellis.values():
            missing_by_page = {page_number: 0
                for page_number in trellis_node.pages}
            neighbors = trellis_node.get_neighbors()
            for neighbor in neighbors:
                for page_number in trellis_node.pages.difference(neighbor.pages):
                    missing_by_page[page_number] += 1
            if any(count for count in missing_by_page.values()):
                trellis_node.node['missingByPage'] = missing_by_page
        for node in nodes.values():
            node['pages'] = tuple(sorted(node['pages']))
        for link in links.values():
            link['pages'] = tuple(sorted(link.get('pages', ())))

    def partition_trellis(self, trellis, nodes, links, verbose=True):
        if verbose:
            print('    Partitioning trellis...')
            max_nodes = self.max_nodes or 100
            max_links = max_nodes * self.link_ratio
            message = '        Maximum: {} / {}'
            message = message.format(max_nodes, max_links)
            print(message)
        page_count = math.ceil(float(len(trellis)) / max_nodes)
        pages = [set() for _ in range(page_count)]
        trellis_nodes_by_distance = self.group_trellis(trellis)
        threshold = len(trellis) / len(pages) / len(trellis_nodes_by_distance)
        winning_distance = self.find_trellis_distance(
            trellis_nodes_by_distance,
            threshold,
            )
        self.page_by_local_neighborhood(pages, trellis, trellis_nodes_by_distance)
        self.page_at_winning_distance(pages, trellis_nodes_by_distance, winning_distance)
        self.page_by_distance(pages, trellis_nodes_by_distance)
        if verbose:
            for i, page in enumerate(pages):
                message = '        Page {}: {}'
                message = message.format(i, len(page))
                print(message)
        return pages

    def postprocess_links(self, links):
        links = tuple(sorted(links.values(),
            key=lambda x: (
                x['source'],
                x['role'],
                x['target'],
                x.get('release_id')
                )))
        for link in links:
            if link['source'][0] == 1:
                link['source'] = 'artist-{}'.format(link['source'][1])
            else:
                link['source'] = 'label-{}'.format(link['source'][1])
            if link['target'][0] == 1:
                link['target'] = 'artist-{}'.format(link['target'][1])
            else:
                link['target'] = 'label-{}'.format(link['target'][1])
        return links

    def postprocess_nodes(self, nodes):
        cluster_count = 0
        cluster_map = {}
        for node in sorted(
            nodes.values(),
            key=lambda x: len(x['aliases']),
            reverse=True,
            ):
            cluster = None
            if node['aliases']:
                if node['id'] not in cluster_map:
                    cluster_count += 1
                    cluster_map[node['id']] = cluster_count
                    for alias_id in node['aliases']:
                        cluster_map[alias_id] = cluster_count
                cluster = cluster_map[node['id']]
            if not node['aliases']:
                del(node['aliases'])
            else:
                node['aliases'] = tuple(sorted(node['aliases']))
            if cluster is not None:
                node['cluster'] = cluster
            node['size'] = len(node.pop('members'))
            node['links'] = tuple(sorted(node['links']))
        nodes = tuple(sorted(nodes.values(),
            key=lambda x: (x['type'], x['id'])))
        return nodes

    def process_relation(
        self,
        distance,
        entity_keys_to_visit,
        links,
        nodes,
        original_roles,
        relation,
        ):
        source = relation['source']
        target = relation['target']
        if source not in nodes:
            entity_keys_to_visit.add(source)
            nodes[source] = self.entity_key_to_node(source, distance + 1)
        if target not in nodes:
            entity_keys_to_visit.add(target)
            nodes[target] = self.entity_key_to_node(target, distance + 1)
        if relation['role'] == 'Alias':
            nodes[source]['aliases'].add(target[1])
            nodes[target]['aliases'].add(source[1])
        elif relation['role'] in ('Member Of', 'Sublabel Of'):
            nodes[target]['members'].add(source[1])
        if relation['role'] not in original_roles:
            return
        link = relation
        link['distance'] = min(
            nodes[source]['distance'],
            nodes[target]['distance'],
            )
        if link['key'] in links and 'releases' in link:
            if 'releases' not in links[link['key']]:
                links[link['key']]['releases'] = link['releases']
            else:
                links[link['key']]['releases'].update(link['releases'])
        else:
            links[link['key']] = link
        nodes[source]['links'].add(link['key'])
        nodes[target]['links'].add(link['key'])

    def prune_excess_links(self, nodes, links, verbose=True):
        max_nodes = self.max_nodes or 100
        max_links = self.link_ratio * max_nodes
        if max_links:
            links_to_prune = sorted(links.values(),
                key=self.link_sorter,
                )[max_links:]
            for link in links_to_prune:
                self.prune_link(link, nodes, links)
        if verbose:
            message = '    Pruned by max links: {} / {}'
            message = message.format(len(nodes), len(links))
            print(message)

    def prune_excess_nodes(self, nodes, links, verbose=True):
        if self.max_nodes:
            nodes_to_prune = sorted(nodes.values(),
                key=lambda x: (x['distance'], x['id']),
                )[self.max_nodes:]
            for node in nodes_to_prune:
                self.prune_node(node, nodes, links)
        if verbose:
            message = '    Pruned by max nodes: {} / {}'
            message = message.format(len(nodes), len(links))
            print(message)

    def prune_link(self, link, nodes, links, update_missing_count=True):
        if link is None:
            return
        if link['key'] in links:
            del(links[link['key']])
        source_node = nodes.get(link['source'])
        if source_node is not None:
            if update_missing_count:
                source_node['missing'] += 1
            if link['key'] in source_node['links']:
                source_node['links'].remove(link['key'])
            if not source_node['links']:
                self.prune_node(source_node, nodes, links,
                    update_missing_count=update_missing_count)
        target_node = nodes.get(link['target'])
        if target_node is not None:
            if update_missing_count:
                target_node['missing'] += 1
            if link['key'] in target_node['links']:
                target_node['links'].remove(link['key'])
            if not target_node['links']:
                self.prune_node(target_node, nodes, links,
                    update_missing_count=update_missing_count)

    def prune_nameless(self, nodes, links, verbose=True):
        for node in tuple(nodes.values()):
            if not node.get('name'):
                self.prune_node(node, nodes, links, update_missing_count=False)
        if verbose:
            message = '    Pruning nameless: {} / {}'
            message = message.format(len(nodes), len(links))
            print(message)

    def prune_not_on_label(self, nodes, links, verbose=True):
        for node in tuple(nodes.values()):
            if 'Not On Label' in node.get('name', ''):
                self.prune_node(node, nodes, links, update_missing_count=False)
        if verbose:
            message = '    Pruning "Not On Label": {} / {}'
            message = message.format(len(nodes), len(links))
            print(message)

    def prune_node(self, node, nodes, links, update_missing_count=True):
        if node is None:
            return
        if node['type'] == 'artist':
            key = (1, node['id'])
        else:
            key = (2, node['id'])
        if key in nodes:
            del(nodes[key])
        for link_key in node['links'].copy():
            link = links.get(link_key)
            self.prune_link(link, nodes, links,
                update_missing_count=update_missing_count)

    def prune_unpaged_links(self, nodes, links, verbose=True):
        print('    Pruning unpaged links...')
        for link_key, link in tuple(links.items()):
            #print('        {}'.format(link))
            if not link['pages']:
                self.prune_link(link, nodes, links)
        if verbose:
            message = '    Pruned unpaged: {} / {}'
            message = message.format(len(nodes), len(links))
            print(message)

    def prune_unvisited(self, entity_keys_to_visit, nodes, links, verbose=True):
        for key in entity_keys_to_visit:
            node = nodes.get(key)
            self.prune_node(node, nodes, links)
        if verbose:
            message = '    Pruned unvisited: {} / {}'
            message = message.format(len(nodes), len(links))
            print(message)

    def query_node_names(self, nodes):
        artist_ids = []
        label_ids = []
        for entity_type, entity_id in nodes.keys():
            if entity_type == 1:
                artist_ids.append(entity_id)
            else:
                label_ids.append(entity_id)
        entity_query_cap = 999 - 1
        entities = []
        for i in range(0, len(artist_ids), entity_query_cap):
            artist_id_slice = artist_ids[i:i + entity_query_cap]
            where_clause = SqliteEntity.entity_type == 1
            where_clause &= SqliteEntity.entity_id.in_(artist_id_slice)
            query = SqliteEntity.select().where(where_clause)
            entities.extend(query)
        for i in range(0, len(label_ids), entity_query_cap):
            label_id_slice = label_ids[i:i + entity_query_cap]
            where_clause = SqliteEntity.entity_type == 2
            where_clause &= SqliteEntity.entity_id.in_(label_id_slice)
            query = SqliteEntity.select().where(where_clause)
            entities.extend(query)
        for entity in entities:
            nodes[(entity.entity_type, entity.entity_id)]['name'] = entity.name

    def query_relations(
        self,
        entity_keys,
        distance=None,
        nodes=None,
        links=None,
        roles=None,
        year=None,
        verbose=True,
        ):
        noncore_roles = list(set(roles) - set(self.core_roles))
        print('        All Roles:', roles)
        print('        Noncore Roles:', noncore_roles)
        max_links = (self.max_nodes or 100) * self.link_ratio
        relations = []
        for entity_key in entity_keys:
            entity_type, entity_id = entity_key
            entity_query = SqliteEntity.select().where(
                SqliteEntity.entity_id == entity_id,
                SqliteEntity.entity_type == entity_type,
                )
            if not entity_query.count():
                continue
            entity = entity_query.get()
            if 'Not On Label' in entity.name:
                print('             Skipping: "Not On Label"')
                continue
            data = []
            core_cache_key = self.make_cache_key(
                'discograph:/api/{entity_type}/neighborhood/{entity_id}',
                entity_type,
                entity_id,
                roles=self.core_roles,
                )
            core_data = self.cache_get(core_cache_key)
            if core_data is None:
                core_query = SqliteRelation.search(
                    entity_id=entity_id,
                    entity_type=entity_type,
                    roles=self.core_roles,
                    query_only=True,
                    )
                core_data = list(core_query)
                self.cache_set(core_cache_key, core_data)
            data.extend(_ for _ in core_data if _.role in roles)
            if noncore_roles:
                noncore_query = SqliteRelation.search(
                    entity_id=entity_id,
                    entity_type=entity_type,
                    roles=noncore_roles,
                    query_only=True,
                    )
                data.extend(noncore_query)
            grouped_data = self.group_relations_for_collection(data)
            if 0 < distance and max_links < len(grouped_data):
                nodes[entity_key]['missing'] += len(grouped_data)
                message = '            Skipping: "{}" w/ {} links'
                message = message.format(entity.name, len(grouped_data))
                print(message)
                continue
            relations.extend(grouped_data)
        #pprint.pprint(relations)
        return relations

    def cross_reference(self, nodes, roles, verbose=True):
        if verbose:
            print('    Cross-referencing artists and labels.')
        root_key = (
            self.center_entity.entity_type,
            self.center_entity.entity_id,
            )
        query_cap = 1000
        query_cap -= 2
        query_cap -= len(roles)
        query_cap //= 2
        artists = []
        labels = []
        grouped_artists = []
        grouped_labels = []
        for key in nodes:
            if key == root_key:
                continue
            if key[0] == 1:
                artists.append(key)
            elif key[0] == 2:
                labels.append(key)
        artists.sort()
        labels.sort()
        for i in range(0, len(artists), query_cap):
            grouped_artists.append(artists[i:i + query_cap])
        for i in range(0, len(labels), query_cap):
            grouped_labels.append(labels[i:i + query_cap])
        iterator = itertools.product(grouped_artists, grouped_labels)
        relations = []
        for artists, labels in iterator:
            #print(len(artists), len(labels))
            found = SqliteRelation.search_bimulti(
                artists,
                labels,
                roles=roles,
                )
            relations.extend(found)
        return relations

    def report_search_start(
        self,
        max_links,
        max_nodes,
        roles,
        verbose=True,
        ):
        if verbose:
            message = '    Max nodes: {}'
            message = message.format(max_nodes)
            print(message)
            message = '    Max links: {}'
            message = message.format(max_links)
            print(message)
            message = '    Roles: {}'
            message = message.format(roles)
            print(message)

    def report_search_loop_start(
        self,
        distance,
        links,
        nodes,
        to_visit,
        verbose=True,
        ):
        if verbose:
            to_visit_count = len(to_visit)
            message = '    At distance {}:'
            message = message.format(distance)
            print(message)
            message = '        {} old nodes'
            message = message.format(len(nodes) - to_visit_count)
            print(message)
            message = '        {} old links'
            message = message.format(len(links))
            print(message)
            message = '        {} new nodes'
            message = message.format(to_visit_count)
            print(message)

    @classmethod
    def make_cache_key(cls, template, entity_type, entity_id, roles=None, year=None):
        if isinstance(entity_type, int):
            entity_type = cls.entity_type_names[entity_type]
        key = template.format(entity_type=entity_type, entity_id=entity_id)
        if roles or year:
            parts = []
            if roles:
                roles = (cls.word_pattern.sub('+', _) for _ in roles)
                roles = ('roles[]={}'.format(_) for _ in roles)
                roles = '&'.join(sorted(roles))
                parts.append(roles)
            if year:
                if isinstance(year, int):
                    year = 'year={}'.format(year)
                else:
                    year = '-'.join(str(_) for _ in year)
                    year = 'year={}'.format(year)
                parts.append(year)
            query_string = '&'.join(parts)
            key = '{}?{}'.format(key, query_string)
        key = 'discograph:{}'.format(key)
        return key

    @classmethod
    def cache_get(cls, key, use_redis=False):
        from discograph import app
        if use_redis:
            cache = app.rcache
        else:
            cache = app.fcache
        data = cache.get(key)
        #print('CACHE GET: {} [{}]'.format(data is not None, key))
        return data

    @classmethod
    def cache_set(cls, key, value, timeout=None, use_redis=False):
        from discograph import app
        if not timeout:
            timeout = 60 * 60 * 24
        if use_redis:
            cache = app.rcache
        else:
            cache = app.fcache
        cache.set(key, value, timeout=timeout)