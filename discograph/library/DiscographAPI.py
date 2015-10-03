# -*- encoding: utf-8 -*-
import os
import random
import re
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
from abjad.tools import systemtools
from werkzeug.contrib.cache import FileSystemCache


class DiscographAPI(object):

    urlify_pattern = re.compile(r"\s+", re.MULTILINE)

    ### INITIALIZER ###

    def __init__(self):
        import discograph
        config_path = os.path.join(
            discograph.__path__[0],
            'configuration',
            'discograph.cfg',
            )
        parser = ConfigParser()
        parser.read(config_path)
        if parser.has_option('url', 'application_url'):
            self._application_url = parser.get('url', 'application_url')
        else:
            self._application_url = ''
        if parser.has_option('cache', 'directory'):
            cache_path = parser.get('cache', 'directory')
        else:
            cache_path = os.path.join('..', 'tmp')
        cache_path = os.path.join(discograph.__path__[0], cache_path)
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        self._cache = FileSystemCache(
            cache_path,
            default_timeout=60 * 60 * 48,
            threshold=1024 * 32,
            )
        #print('Clearing cache.')
        #self._cache.clear()

    ### PUBLIC METHODS ###

    def cache_get(self, cache_key):
        data = self.cache.get(cache_key)
        if data is not None:
            print('Cache Hit:  {}'.format(cache_key))
            return data
        print('Cache Miss: {}'.format(cache_key))

    def cache_set(self, cache_key, data):
        self.cache.set(cache_key, data)

    def get_network(self, entity_id, entity_type, on_mobile=False):
        import discograph
        cache_key = 'discograph:/api/artist/network/{}'.format(entity_id)
        if on_mobile:
            cache_key = '{}/mobile'.format(cache_key)
        data = self.cache_get(cache_key)
        if data is not None:
            return data
        artist = self.get_entity(entity_id, 1)
        if artist is None:
            return None
        role_names = [
            'Alias',
            'Member Of',
            #'Producer',
            #'Guitar',
            #'Bass Guitar',
            #'Rhythm Guitar',
            #'Electric Guitar',
            #'Lead Guitar',
            #'Drums',
            #'Vocals',
            #'Lead Vocals',
            #'Backing Vocals',
            ]
        if not on_mobile:
            max_nodes = 75
            max_links = 200
            degree = 12
        else:
            max_nodes = 25
            max_links = 75
            degree = 6
        relation_grapher = discograph.RelationGrapher(
            center_entity=artist,
            degree=degree,
            max_nodes=max_nodes,
            max_links=max_links,
            role_names=role_names,
            )
        with systemtools.Timer(exit_message='Network query time:'):
            data = relation_grapher.get_network()
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
        query = discograph.SqliteFTSArtist.search_bm25(search_string).limit(10)
        data = []
        for sql_fts_artist in query:
            datum = dict(
                key='artist-{}'.format(sql_fts_artist.id),
                name=sql_fts_artist.name,
                )
            data.append(datum)
            print('    {}'.format(datum))
        data = {'results': tuple(data)}
        self.cache_set(cache_key, data)
        return data

    ### PUBLIC PROPERTIES ###

    @property
    def application_url(self):
        return self._application_url

    @property
    def cache(self):
        return self._cache