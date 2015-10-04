# -*- encoding: utf-8 -*-
import collections
import re
import six
from discograph.library.TrellisNode import TrellisNode
from discograph.library.mongo.CreditRole import CreditRole
from discograph.library.sqlite.SqliteEntity import SqliteEntity
from discograph.library.sqlite.SqliteRelation import SqliteRelation


class RelationGrapher(object):

    ### CLASS VARIABLES ###

    word_pattern = re.compile('\s+')

    ### INITIALIZER ###

    def __init__(
        self,
        center_entity,
        cache=None,
        degree=3,
        max_links=None,
        max_nodes=None,
        role_names=None,
        year=None,
        ):
        assert isinstance(center_entity, SqliteEntity)
        self.center_entity = center_entity
        degree = int(degree)
        assert 0 < degree
        self.degree = degree
        self.cache = cache
        if max_links is not None:
            max_links = int(max_links)
            assert 0 < max_links
        self.max_links = max_links
        if max_nodes is not None:
            max_nodes = int(max_nodes)
            assert 0 < max_nodes
        self.max_nodes = max_nodes
        role_names = role_names or None
        if role_names:
            if isinstance(role_names, six.string_types):
                role_names = (role_names,)
            elif not isinstance(role_names, collections.Iterable):
                role_names = (role_names,)
            role_names = tuple(role_names)
            assert all(_ in CreditRole.all_credit_roles
                for _ in role_names)
        self.role_names = role_names
        if year is not None:
            if isinstance(year, collections.Sequence):
                year = tuple(int(_) for _ in year)
                assert len(year) == 2
            else:
                year = int(year)
        self.year = year

    def build_trellis(self, nodes, links, verbose=True):
        if verbose:
            print('    Building paging tree')
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
        return trellis

    def collect_entities(self, verbose=True):
        original_role_names = self.role_names or ()
        print('Roles:', original_role_names)
        provisional_role_names = set(original_role_names)
        provisional_role_names.update(['Alias', 'Member Of'])
        provisional_role_names = sorted(provisional_role_names)
        initial_key = (
            self.center_entity.entity_type,
            self.center_entity.entity_id,
            )
        entity_keys_to_visit = set([initial_key])
        links = dict()
        nodes = dict()
        break_on_next_loop = False
        distance_pruned_roles = {
            0: ['Released On', 'Compiled On'],
            1: ['Producer', 'Remix', 'DJ Mix'],
            }
        for distance in range(self.degree + 1):
            current_entity_keys_to_visit = list(entity_keys_to_visit)
            for key in current_entity_keys_to_visit:
                nodes.setdefault(key, self.entity_key_to_node(key, distance))
            if verbose:
                print('    At distance {}:'.format(distance))
                print('        {} old nodes'.format(
                    len(nodes) - len(current_entity_keys_to_visit)))
                print('        {} old links'.format(len(links)))
                print('        {} new nodes'.format(
                    len(current_entity_keys_to_visit)))
            if break_on_next_loop:
                if verbose:
                    print('        Exiting search loop.')
                break
            if 1 < distance:
                if self.max_nodes and self.max_nodes <= len(nodes):
                    if verbose:
                        print('        Max nodes: exiting next search loop.')
                    break_on_next_loop = True
            relations = self.query_relations(
                entity_keys=current_entity_keys_to_visit,
                role_names=provisional_role_names,
                year=None,
                verbose=verbose,
                )
            for role_name in distance_pruned_roles.get(distance, []):
                if role_name in provisional_role_names:
                    provisional_role_names.remove(role_name)
            if verbose:
                print('            {} new links'.format(len(relations)))
            if not relations:
                break_on_next_loop = True
            if 0 < distance:
                if self.max_links and (self.max_links * 2) <= len(relations):
                    if verbose:
                        print('        Max links: exiting next search loop.')
                    break_on_next_loop = True
            entity_keys_to_visit.clear()
            for relation in relations:
                self.process_relation(
                    distance=distance,
                    entity_keys_to_visit=entity_keys_to_visit,
                    links=links,
                    nodes=nodes,
                    original_role_names=original_role_names,
                    relation=relation,
                    )
        if verbose:
            print('    Collected: {} / {}'.format(len(nodes), len(links)))
        self.query_node_names(nodes)
        self.prune_nameless(nodes, links, verbose=verbose)
        trellis = self.build_trellis(nodes, links, verbose=verbose)
        self.prune_unvisited(entity_keys_to_visit, nodes, links, verbose=verbose)
        self.prune_excess_nodes(nodes, links, verbose=verbose)
        self.prune_excess_links(nodes, links, verbose=verbose)
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
        cluster_count = 0
        cluster_map = {}
        for node in nodes.values():
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
        nodes = tuple(sorted(nodes.values(),
            key=lambda x: (x['type'], x['id'])))
        if self.center_entity.entity_type == 1:
            center = 'artist-{}'.format(self.center_entity.entity_id)
        elif self.center_entity.entity_type == 2:
            center = 'label-{}'.format(self.center_entity.discogs_id)
        else:
            raise ValueError(self.center_entity)
        network = {
            'center': center,
            'nodes': nodes,
            'links': links,
            }
        return network

    @staticmethod
    def link_sorter(link):
        role = 2
        if link['role'] == 'Alias':
            role = 0
        elif link['role'] == 'Member Of':
            role = 1
        return link['distance'], role, link['key']

    def process_relation(
        self,
        distance,
        entity_keys_to_visit,
        links,
        nodes,
        original_role_names,
        relation,
        ):
        e1k = (relation.entity_one_type, relation.entity_one_id)
        e2k = (relation.entity_two_type, relation.entity_two_id)
        if e1k not in nodes:
            entity_keys_to_visit.add(e1k)
            nodes[e1k] = self.entity_key_to_node(e1k, distance + 1)
        if e2k not in nodes:
            entity_keys_to_visit.add(e2k)
            nodes[e2k] = self.entity_key_to_node(e2k, distance + 1)
        if relation.role_name == 'Alias':
            nodes[e1k]['aliases'].add(e2k[1])
            nodes[e2k]['aliases'].add(e1k[1])
        elif relation.role_name in ('Member Of', 'Sublabel Of'):
            nodes[e2k]['members'].add(e1k[1])
        if relation.role_name not in original_role_names:
            return
        link = dict(
            role=relation.role_name,
            source=e1k,
            target=e2k,
            )
        if relation.release_id:
            link['release_id'] = relation.release_id
        if relation.year:
            link['year'] = relation.year
        link['distance'] = min(
            nodes[e1k]['distance'],
            nodes[e2k]['distance'],
            )
        link['key'] = self.get_link_key(link)
        links[link['key']] = link
        nodes[e1k]['links'].add(link['key'])
        nodes[e2k]['links'].add(link['key'])

    def prune_excess_links(self, nodes, links, verbose=True):
        if self.max_links:
            links_to_prune = sorted(links.values(),
                key=self.link_sorter,
                )[self.max_links:]
            for link in links_to_prune:
                self.prune_link(link, nodes, links)
        if verbose:
            print('    Pruned by max links: {} / {}'.format(len(nodes), len(links)))

    def prune_excess_nodes(self, nodes, links, verbose=True):
        if self.max_nodes:
            nodes_to_prune = sorted(nodes.values(),
                key=lambda x: (x['distance'], x['id']),
                )[self.max_nodes:]
            for node in nodes_to_prune:
                self.prune_node(node, nodes, links)
        if verbose:
            print('    Pruned by max nodes: {} / {}'.format(len(nodes), len(links)))

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
            print('    Pruning nameless: {} / {}'.format(len(nodes), len(links)))

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

    def prune_unvisited(self, entity_keys_to_visit, nodes, links, verbose=True):
        for key in entity_keys_to_visit:
            node = nodes.get(key)
            self.prune_node(node, nodes, links)
        if verbose:
            print('    Pruned unvisited: {} / {}'.format(len(nodes), len(links)))

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
            where_clause = SqliteEntity.entity_type == 1
            where_clause &= SqliteEntity.entity_id.in_(artist_ids[i:i + entity_query_cap])
            query = SqliteEntity.select().where(where_clause)
            entities.extend(query)
        for i in range(0, len(label_ids), entity_query_cap):
            where_clause = SqliteEntity.entity_type == 2
            where_clause &= SqliteEntity.entity_id.in_(label_ids[i:i + entity_query_cap])
            query = SqliteEntity.select().where(where_clause)
            entities.extend(query)
        for entity in entities:
            nodes[(entity.entity_type, entity.entity_id)]['name'] = entity.name

    def query_relations(self, entity_keys, role_names=None, year=None, verbose=True):
        print('        Roles:', role_names)
        entity_query_cap = 999
        entity_query_cap -= (1 + len(role_names)) * 2
        if isinstance(year, int):
            entity_query_cap -= 2
        elif year:
            entity_query_cap -= 4
        entity_query_cap //= 2
        range_stop = len(entity_keys)
        relations = []
        for start in range(0, range_stop, entity_query_cap):
            stop = start + entity_query_cap
            entity_key_slice = entity_keys[start:stop]
            found = SqliteRelation.search_multi(
                entity_key_slice,
                role_names=role_names,
                verbose=verbose,
                year=year,
                )
            relations.extend(found)
        return relations