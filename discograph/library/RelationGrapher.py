# -*- encoding: utf-8 -*-
import collections
import re
import six
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
        return '{}-{}-{}-{}-{}'.format(
            source_type,
            source_id,
            cls.word_pattern.sub('-', link['role']).lower(),
            target_type,
            target_id,
            )

    def relation_to_link(self, relation):
        link = relation.copy()
        entity_one_id = link['entity_one_id']
        entity_one_type = link['entity_one_type']
        source_key = (entity_one_type, entity_one_id)
        link['source'] = source_key
        entity_two_id = link['entity_two_id']
        entity_two_type = link['entity_two_type']
        target_key = (entity_two_type, entity_two_id)
        link['target'] = target_key
        link['role'] = link['role_name']
        link['key'] = self.get_link_key(link)
        if '_id' in link: del(link['_id'])
        if 'country' in link: del(link['country'])
        if 'entity_one_id' in link: del(link['entity_one_id'])
        if 'entity_one_type' in link: del(link['entity_one_type'])
        if 'entity_two_id' in link: del(link['entity_two_id'])
        if 'entity_two_type' in link: del(link['entity_two_type'])
        if 'id' in link: del(link['id'])
        if 'role_name' in link: del(link['role_name'])
        if 'category' in link and not link.get('category'):
            del(link['category'])
        if 'subcategory' in link and not link.get('subcategory'):
            del(link['subcategory'])
        if 'genres' in link and not link.get('genres'):
            del(link['genres'])
        if 'random' in link:
            del(link['random'])
        if 'release_id' in link and not link.get('release_id'):
            del(link['release_id'])
        if 'styles' in link and not link.get('styles'):
            del(link['styles'])
        if 'year' in link and not link.get('year'):
            del(link['year'])
        return link

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

    def collect_entities(self):
        original_role_names = self.role_names or ()
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

        entity_query_cap = 999
        entity_query_cap -= (1 + len(provisional_role_names)) * 2
        entity_query_cap //= 2

        break_on_next_loop = False

        for distance in range(self.degree + 1):

            current_entity_keys_to_visit = list(entity_keys_to_visit)
            for key in current_entity_keys_to_visit:
                nodes.setdefault(key, self.entity_key_to_node(key, distance))

            #print('    At distance {}:'.format(distance))
            #print('        {} new nodes'.format(
            #    len(current_entity_keys_to_visit)))
            #print('        {} old nodes'.format(
            #    len(nodes) - len(current_entity_keys_to_visit)))
            #print('        {} old links'.format(len(links)))

            if break_on_next_loop:
                #print('        Leaving search loop.')
                break
            if (
                1 < distance and
                self.max_nodes and
                self.max_nodes <= len(nodes)
                ):
                #print('        Maxed out node count.')
                break_on_next_loop = True

            entity_keys_to_visit.clear()
            relations = []
            range_stop = len(current_entity_keys_to_visit)
            for start in range(0, range_stop, entity_query_cap):
                # Split into multiple queries to avoid variable maximum.
                stop = start + entity_query_cap
                #print('        Querying: {} to {} of {} new nodes'.format(
                #    start, stop, len(current_entity_keys_to_visit)
                #    ))
                entity_key_slice = current_entity_keys_to_visit[start:stop]
                relations.extend(SqliteRelation.search_multi(
                    entity_key_slice,
                    role_names=provisional_role_names,
                    ))
            for relation in relations:
                e1k = (relation['entity_one_type'], relation['entity_one_id'])
                e2k = (relation['entity_two_type'], relation['entity_two_id'])
                if e1k not in nodes:
                    entity_keys_to_visit.add(e1k)
                    nodes[e1k] = self.entity_key_to_node(e1k, distance + 1)
                if e2k not in nodes:
                    entity_keys_to_visit.add(e2k)
                    nodes[e2k] = self.entity_key_to_node(e2k, distance + 1)
                if relation['role_name'] == 'Alias':
                    nodes[e1k]['aliases'].add(e2k[1])
                    nodes[e2k]['aliases'].add(e1k[1])
                elif relation['role_name'] in ('Member Of', 'Sublabel Of'):
                    nodes[e2k]['members'].add(e1k[1])
                if relation['role_name'] not in original_role_names:
                    continue
                link = self.relation_to_link(relation)
                link['distance'] = min(
                    nodes[e1k]['distance'],
                    nodes[e2k]['distance'],
                    )
                links[link['key']] = link
                nodes[e1k]['links'].add(link['key'])
                nodes[e2k]['links'].add(link['key'])

        #print('    Collected: {} / {}'.format(len(nodes), len(links)))

        # Query node names.
        artist_ids = []
        label_ids = []
        for entity_type, entity_id in nodes.keys():
            if entity_type == 1:
                artist_ids.append(entity_id)
            else:
                label_ids.append(entity_id)
        artists = []
        entity_query_cap = 999
        entity_query_cap -= 1
        for i in range(0, len(artist_ids), entity_query_cap):
            where_clause = SqliteEntity.entity_id.in_(artist_ids[i:i + entity_query_cap])
            where_clause &= SqliteEntity.entity_type == 1
            query = SqliteEntity.select().where(where_clause)
            artists.extend(query)
        labels = []
        for i in range(0, len(artist_ids), entity_query_cap):
            where_clause = SqliteEntity.entity_id.in_(label_ids[i:i + entity_query_cap])
            where_clause &= SqliteEntity.entity_type == 2
            query = SqliteEntity.select().where(where_clause)
            labels.extend(query)
        for artist in artists:
            nodes[(artist.entity_type, artist.entity_id)]['name'] = artist.name
        for label in labels:
            nodes[(label.entity_type, label.entity_id)]['name'] = label.name

        # Prune nameless nodes.
        for node in tuple(nodes.values()):
            if not node.get('name'):
                self.prune_node(node, nodes, links, update_missing_count=False)
        #print('    Pruning nameless: {} / {}'.format(len(nodes), len(links)))

        # Prune unvisited nodes and links.
        for key in entity_keys_to_visit:
            node = nodes.get(key)
            self.prune_node(node, nodes, links)
        #print('    Pruned unvisited: {} / {}'.format(
        #    len(nodes), len(links)))

        # Prune nodes beyond maximum.
        if self.max_nodes:
            nodes_to_prune = sorted(nodes.values(),
                key=lambda x: (x['distance'], x['id']),
                )[self.max_nodes:]
            for node in nodes_to_prune:
                self.prune_node(node, nodes, links)
        #print('    Pruned by max nodes: {} / {}'.format(
        #    len(nodes), len(links)))

        # Prune links beyond maximum.
        if self.max_links:
            links_to_prune = sorted(links.values(),
                key=self.link_sorter,
                )[self.max_links:]
            for link in links_to_prune:
                self.prune_link(link, nodes, links)
        #print('    Pruned by max links: {} / {}'.format(
        #    len(nodes), len(links)))

        #print('Finally: {} / {}'.format(len(nodes), len(links)))
        return nodes, links

    def prune_link(self, link, nodes, links, update_missing_count=True):
        if link is None:
            return
        if link['key'] in links:
            del(links[link['key']])
        source_node = nodes.get(link['source'])
        if source_node is not None:
            if update_missing_count:
                source_node['missing'] += 1
            source_node['links'].remove(link['key'])
            if not source_node['links']:
                self.prune_node(source_node, nodes, links,
                    update_missing_count=update_missing_count)
        target_node = nodes.get(link['target'])
        if target_node is not None:
            if update_missing_count:
                target_node['missing'] += 1
            target_node['links'].remove(link['key'])
            if not target_node['links']:
                self.prune_node(target_node, nodes, links,
                    update_missing_count=update_missing_count)

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
            center = 'label-{}'.format(self.center_entity.entity_id)
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