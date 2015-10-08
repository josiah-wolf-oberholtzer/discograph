# -*- encoding: utf-8 -*-
import random
import re
from abjad.tools import systemtools


class DiscographAPI(object):

    urlify_pattern = re.compile(r"\s+", re.MULTILINE)

    ### PUBLIC METHODS ###

    def cache_get(self, cache_key):
        from discograph import app
        data = app.cache.get(cache_key)
        if data is not None:
            print('Cache Hit:  {}'.format(cache_key))
            return data
        print('Cache Miss: {}'.format(cache_key))

    def cache_set(self, cache_key, data):
        from discograph import app
        app.cache.set(cache_key, data)

    def get_network(self, entity_id, entity_type, on_mobile=False, cache=True):
        import discograph
        assert entity_type in ('artist', 'label')
        if cache:
            cache_key = 'discograph:/api/{}/network/{}'.format(entity_type, entity_id)
            if on_mobile:
                cache_key = '{}/mobile'.format(cache_key)
            data = self.cache_get(cache_key)
            if data is not None:
                return data
        if entity_type == 'artist':
            entity_type = 1
        elif entity_type == 'label':
            entity_type = 2
        else:
            raise ValueError(entity_type)
        entity = self.get_entity(entity_id, 1)
        if entity is None:
            return None
        role_names = [
            'Alias',
            'Member Of',
            ]
        if not on_mobile:
            max_nodes = 75
            degree = 12
        else:
            max_nodes = 25
            degree = 6
        relation_grapher = discograph.RelationGrapher(
            center_entity=entity,
            degree=degree,
            max_nodes=max_nodes,
            role_names=role_names,
            )
        with systemtools.Timer(exit_message='Network query time:'):
            data = relation_grapher.get_network()
        if cache:
            self.cache_set(cache_key, data)
        return data

    def get_entity(self, entity_id, entity_type):
        import discograph
        if entity_type == 'artist':
            entity_type = 1
        elif entity_type == 'label':
            entity_type = 2
        where_clause = discograph.SqliteEntity.entity_id == entity_id
        where_clause &= discograph.SqliteEntity.entity_type == entity_type
        query = discograph.SqliteEntity.select().where(where_clause)
        found = list(query)
        if not found:
            return None
        return found[0]

    def get_random_entity(self, role_names=None):
        import discograph
        relation = discograph.SqliteRelation.get_random(role_names=role_names)
        entity_choice = random.randint(1, 2)
        if entity_choice == 1:
            entity_type = relation.entity_one_type
            entity_id = relation.entity_one_id
        else:
            entity_type = relation.entity_two_type
            entity_id = relation.entity_two_id
        return entity_type, entity_id

    def search_entities(self, search_string):
        import discograph
        cache_key = 'discograph:/api/search/{}'.format(
            self.urlify_pattern.sub('+', search_string))
        data = self.cache_get(cache_key)
        if data is not None:
            return data
        query = discograph.SqliteFTSEntity.search_bm25(search_string)
        query = query.where(discograph.SqliteFTSEntity.entity_type == 1)
        query = query.limit(10)
        data = []
        entity_type_names = {1: 'artist', 2: 'label'}
        for entity in query:
            datum = dict(
                key='{}-{}'.format(
                    entity_type_names[entity.entity_type],
                    entity.entity_id,
                    ),
                name=entity.name,
                )
            data.append(datum)
            print('    {}'.format(datum))
        data = {'results': tuple(data)}
        self.cache_set(cache_key, data)
        return data