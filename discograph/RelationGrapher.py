# -*- encoding: utf-8 -*-
import collections
import mongoengine
import re
import six
from abjad.tools import systemtools
from discograph import models


class RelationGrapher(object):

    ### CLASS VARIABLES ###

    word_pattern = re.compile('\s+')

    ### INITIALIZER ###

    def __init__(
        self,
        entities,
        cache=None,
        degree=3,
        max_nodes=None,
        role_names=None,
        ):
        prototype = (models.Artist, models.Label)
        if not isinstance(entities, collections.Iterable):
            entities = [entities]
        entities = tuple(entities)
        assert all(isinstance(_, prototype) for _ in entities)
        self.entities = entities
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
            assert all(_ in models.ArtistRole._available_credit_roles
                for _ in role_names)
        self.role_names = role_names

    def can_continue_searching(self, distance, entities_visited):
        if not self.max_nodes:
            return True
        elif 1 < distance and self.max_nodes <= len(entities_visited):
            return False
        return True

    def collect_entities(self):
        entities_visited = dict()
        entities_to_visit = set(
            (type(_).__name__.lower(), _.discogs_id)
            for _ in self.entities,
            )
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
                    entity_cls = models.Artist
                elif entity_type == 'label':
                    entity_cls = models.Label
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
        return '{}-{}-{}-{}-{}'.format(
            link['source'][0],
            link['source'][1],
            cls.word_pattern.sub('-', link['role']).lower(),
            link['target'][0],
            link['target'][1],
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
        if isinstance(entity, models.Artist):
            generator = (_ for _ in entity.members if _.discogs_id)
            neighborhood['size'] = len(tuple(generator))
            generator = (_.discogs_id for _ in entity.aliases if _.discogs_id)
            neighborhood['aliases'] = tuple(generator)
        elif isinstance(entity, models.Label):
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
                    entity_one_type = models.Relation.EntityType(entity_one_type)
                    entity_one_type = entity_one_type.name.lower()
                    source_key = (entity_one_type, entity_one_id)
                    link['source'] = source_key

                    entity_two_id = link['entity_two_id']
                    entity_two_type = link['entity_two_type']
                    entity_two_type = models.Relation.EntityType(entity_two_type)
                    entity_two_type = entity_two_type.name.lower()
                    target_key = (entity_two_type, entity_two_id)
                    link['target'] = target_key

                    del(link['entity_one_id'])
                    del(link['entity_one_type'])
                    del(link['entity_two_id'])
                    del(link['entity_two_type'])
                    link['role'] = link['role_name']
                    del(link['role_name'])

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
        center = tuple(
            '{}-{}'.format(type(_).__name__.lower(), _.discogs_id)
            for _ in self.entities
            )
        network = {
            'center': center,
            'nodes': nodes,
            'links': links,
            }
        return network

    @classmethod
    def query_relations(cls, entity, role_names=None):
        entity_type = models.Relation._model_to_entity_type[type(entity)]
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
        query = models.Relation.objects(q_l | q_r)
        return query