# -*- encoding: utf-8 -*-
import collections
import mongoengine
import re
import six
from abjad.tools import systemtools
from discograph.library.Artist import Artist
from discograph.library.ArtistRole import ArtistRole
from discograph.library.Label import Label
from discograph.library.Relation import Relation
from discograph.library.SQLArtist import SQLArtist
from discograph.library.SQLLabel import SQLLabel
from discograph.library.SQLRelation import SQLRelation


class RelationGrapher(object):

    ### CLASS VARIABLES ###

    word_pattern = re.compile('\s+')

    ### INITIALIZER ###

    def __init__(
        self,
        center_entity,
        cache=None,
        degree=3,
        max_nodes=None,
        role_names=None,
        ):
        prototype = (Artist, Label)
        assert isinstance(center_entity, prototype)
        self.center_entity = center_entity
        degree = int(degree)
        assert 0 < degree
        self.degree = degree
        self.cache = cache
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
            assert all(_ in ArtistRole._available_credit_roles
                for _ in role_names)
        self.role_names = role_names

    def can_continue_searching(self, distance, entities_visited):
        if not self.max_nodes:
            return True
        elif 1 < distance and self.max_nodes <= len(entities_visited):
            return False
        return True

    def collect_entities(self):
        initial_key = (
            type(self.center_entity).__name__.lower(),
            self.center_entity.discogs_id,
            )
        entities_to_visit = set([initial_key])
        entities_visited = dict()
        original_entities = entities_to_visit.copy()
        for distance in range(self.degree + 1):
            current_entities_to_visit = sorted(entities_to_visit)
            entities_to_visit.clear()
            #print('ROUND', distance, current_entities_to_visit)
            #print(current_entities_to_visit)
            while current_entities_to_visit:
                if not self.can_continue_searching(distance, entities_visited):
                    #print('DONE', len(entities_visited))
                    return entities_visited
                entity_key = current_entities_to_visit.pop()
                if entity_key in entities_visited:
                    #print('already visited', entity_key)
                    continue
                entity_type, entity_id = entity_key
                if entity_type == 'artist':
                    entity_cls = Artist
                elif entity_type == 'label':
                    entity_cls = Label
                found_entity = list(entity_cls.objects(discogs_id=entity_id))
                if not found_entity:
                    print('Missing {} ID: {!r}'.format(
                        entity_cls.__name__,
                        entity_id,
                        ))
                    continue
                entity = found_entity[0]
                no_query = False
                if (
                    entity_type == 'label' and
                    entity_key not in original_entities
                    ):
                    #print('skipping', entity_key)
                    if 'Not On Label' in entity.name:
                        #print('white label', entity_key)
                        continue
                    no_query = True
                neighborhood = self.get_neighborhood(
                    entity,
                    cache=self.cache,
                    role_names=self.role_names,
                    no_query=no_query,
                    )
                neighborhood['distance'] = distance
                entities_visited[entity_key] = neighborhood
                entities_to_visit.update(neighborhood['nodes'])
        #print('DONE', len(entities_visited))
        return entities_visited

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

    @classmethod
    def get_node_key(cls, node):
        return '{}-{}'.format(node['type'], node['id'])

    @classmethod
    def get_neighborhood_cache_key(cls, entity, role_names=None):
        key = 'cache:/api/{}/neighborhood/{}'
        key = key.format(type(entity).__name__.lower(), entity.discogs_id)
        if role_names:
            pattern = cls.word_pattern
            role_name_keys = (_.lower() for _ in role_names)
            role_name_keys = (pattern.sub('-', _) for _ in role_name_keys)
            role_name_keys = sorted(role_name_keys)
            key = '{}?role_names={}'.format(key, '+'.join(role_name_keys))
        return key

    @classmethod
    def get_neighborhood(
        cls,
        entity,
        cache=None,
        role_names=None,
        no_query=None,
        ):
        key = cls.get_neighborhood_cache_key(entity, role_names=role_names)
        if not no_query and cache is not None:
            neighborhood = cache.get(key)
            if neighborhood is not None:
                print('    NEIGHBORHOOD CACHE HIT!', entity.discogs_id)
                return neighborhood
            else:
                print('    NEIGHBORHOOD CACHE MISS!', entity.discogs_id)
        neighborhood = {
            'id': entity.discogs_id,
            'type': type(entity).__name__.lower(),
            'name': entity.name,
            }
        if isinstance(entity, Artist):
            generator = (_ for _ in entity.members if _.discogs_id)
            neighborhood['size'] = len(tuple(generator))
            generator = (_.discogs_id for _ in entity.aliases if _.discogs_id)
            neighborhood['aliases'] = tuple(generator)
        elif isinstance(entity, Label):
            generator = (_ for _ in entity.sublabels if _.discogs_id)
            neighborhood['size'] = len(tuple(generator))
        nodes = set()
        if not no_query:
            with systemtools.Timer(exit_message='    Neighborhood query time:'):
                query = cls.query_relations(entity, role_names=role_names)
                links = tuple(query.as_pymongo())
            processed_links = []
            for link in links:
                try:

                    entity_one_id = link['entity_one_id']
                    entity_one_type = link['entity_one_type']
                    entity_one_type = Relation.EntityType(entity_one_type)
                    entity_one_type = entity_one_type.name.lower()
                    source_key = (entity_one_type, entity_one_id)
                    link['source'] = source_key

                    entity_two_id = link['entity_two_id']
                    entity_two_type = link['entity_two_type']
                    entity_two_type = Relation.EntityType(entity_two_type)
                    entity_two_type = entity_two_type.name.lower()
                    target_key = (entity_two_type, entity_two_id)
                    link['target'] = target_key

                    link['role'] = link['role_name']

                    del(link['_id'])
                    del(link['category'])
                    del(link['country'])
                    del(link['entity_one_id'])
                    del(link['entity_one_type'])
                    del(link['entity_two_id'])
                    del(link['entity_two_type'])
                    del(link['role_name'])
                    del(link['subcategory'])

                    if link.get('genres') is None:
                        del(link['genres'])
                    if link.get('styles') is None:
                        del(link['styles'])
                    if link.get('release_id') is None:
                        del(link['release_id'])
                    if link.get('year') is None:
                        del(link['year'])

                    nodes.update((source_key, target_key))
                    processed_links.append(link)
                except Exception as e:
                    #print(link)
                    raise e
            neighborhood['nodes'] = tuple(sorted(nodes))
            neighborhood['links'] = tuple(processed_links)
        else:
            neighborhood['nodes'] = ()
            neighborhood['links'] = ()
        if not no_query and cache is not None:
            cache.set(key, neighborhood)
        return neighborhood

    def relation_to_link(self, relation):
        link = relation.copy()

        entity_one_id = link['entity_one_id']
        entity_one_type = link['entity_one_type']
        #entity_one_type = Relation.EntityType(entity_one_type)
        #entity_one_type = entity_one_type.name.lower()
        source_key = (entity_one_type, entity_one_id)
        link['source'] = source_key

        entity_two_id = link['entity_two_id']
        entity_two_type = link['entity_two_type']
        #entity_two_type = Relation.EntityType(entity_two_type)
        #entity_two_type = entity_two_type.name.lower()
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

    def get_network(self):
        entities = self.collect_entities()
        nodes = []
        links = {}
        cluster_count = 0
        cluster_map = {}
        for entity_key, entity_dict in sorted(entities.items()):
            missing = 0
            for link in entity_dict['links']:
                if link['source'] in entities and link['target'] in entities:
                    link_key = self.get_link_key(link)
                    link['key'] = link_key
                    links[link_key] = link
                else:
                    missing += 1
            cluster = None
            if 'aliases' in entity_dict and entity_dict['aliases']:
                if entity_dict['id'] not in cluster_map:
                    cluster_count += 1
                    cluster_map[entity_dict['id']] = cluster_count
                    for alias_id in entity_dict['aliases']:
                        cluster_map[alias_id] = cluster_count
                cluster = cluster_map[entity_dict['id']]
            node = {
                'distance': entity_dict['distance'],
                'group': cluster,
                'id': entity_dict['id'],
                'key': self.get_node_key(entity_dict),
                'missing': missing,
                'name': entity_dict['name'],
                'size': entity_dict['size'],
                'type': entity_dict['type'],
                }
            nodes.append(node)
        links = tuple(sorted(links.values(),
            key=lambda x: (x['source'], x['role'], x['target'])))
        for link in links:
            link['source'] = '{}-{}'.format(*link['source'])
            link['target'] = '{}-{}'.format(*link['target'])
        nodes = tuple(sorted(nodes, key=lambda x: (x['type'], x['id'])))
        center = '{}-{}'.format(
            type(self.center_entity).__name__.lower(),
            self.center_entity.discogs_id,
            )
        network = {
            'center': center,
            'nodes': nodes,
            'links': links,
            }
        return network

    @classmethod
    def query_relations(cls, entity, role_names=None):
        entity_type = Relation._model_to_entity_type[type(entity)]
        if role_names:
            q_l = mongoengine.Q(
                entity_one_id=entity.discogs_id,
                entity_one_type=entity_type,
                role_name__in=role_names,
                )
            q_r = mongoengine.Q(
                entity_two_id=entity.discogs_id,
                entity_two_type=entity_type,
                role_name__in=role_names,
                )
        else:
            q_l = mongoengine.Q(
                entity_one_id=entity.discogs_id,
                entity_one_type=entity_type,
                )
            q_r = mongoengine.Q(
                entity_two_id=entity.discogs_id,
                entity_two_type=entity_type,
                )
        query = Relation.objects(q_l | q_r)
        return query

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

    def collect_entities_2(self):

        original_role_names = self.role_names or ()
        provisional_role_names = set(original_role_names)
        provisional_role_names.update(['Alias', 'Member Of'])
        provisional_role_names = sorted(provisional_role_names)

        if type(self.center_entity).__name__.endswith('Artist'):
            initial_key = (1, self.center_entity.discogs_id)
        else:
            initial_key = (2, self.center_entity.discogs_id)
        entity_keys_to_visit = set([initial_key])

        links = dict()
        nodes = dict()

        for distance in range(self.degree + 1):
            current_entity_keys_to_visit = list(entity_keys_to_visit)
            for key in current_entity_keys_to_visit:
                nodes.setdefault(key, self.entity_key_to_node(key, distance))
            entity_keys_to_visit.clear()
            relations = SQLRelation.search_multi(
                current_entity_keys_to_visit,
                role_names=provisional_role_names,
                )
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
                    #print(relation)
                    nodes[e2k]['members'].add(e1k[1])
                if relation['role_name'] not in original_role_names:
                    continue
                link = self.relation_to_link(relation)
                links[link['key']] = link
                nodes[e1k]['links'].add(link['key'])
                nodes[e2k]['links'].add(link['key'])

        # Query node names.
        artist_ids = []
        label_ids = []
        for entity_type, entity_id in nodes.keys():
            if entity_type == 1:
                artist_ids.append(entity_id)
            else:
                label_ids.append(entity_id)
        artists = SQLArtist.select().where(SQLArtist.id.in_(artist_ids))
        labels = SQLLabel.select().where(SQLLabel.id.in_(label_ids))
        for artist in artists:
            nodes[(1, artist.id)]['name'] = artist.name
        for label in labels:
            nodes[(2, label.id)]['name'] = label.name

        # Prune unvisited nodes and links.
        for key in entity_keys_to_visit:
            node = nodes.pop(key)
            #print(node['key'], node['name'])
            for link_key in node['links']:
                link = links[link_key]
                source_key = link['source']
                if source_key in nodes:
                    source_node = nodes[link['source']]
                    source_node['missing'] += 1
                    source_node['links'].remove(link_key)
                target_key = link['target']
                if target_key in nodes:
                    target_node = nodes[link['target']]
                    target_node['missing'] += 1
                    target_node['links'].remove(link_key)
                del(links[link_key])

        return nodes, links

    def get_network_2(self):
        nodes, links = self.collect_entities_2()
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
            key=lambda x: (x['source'], x['role'], x['target'])))
        for link in links:
            link['source'] = '{}-{}'.format(*link['source'])
            link['target'] = '{}-{}'.format(*link['target'])
        nodes = tuple(sorted(nodes.values(), key=lambda x: (x['type'], x['id'])))
        center = '{}-{}'.format(
            type(self.center_entity).__name__.lower(),
            self.center_entity.discogs_id,
            )
        network = {
            'center': center,
            'nodes': nodes,
            'links': links,
            }
        return network