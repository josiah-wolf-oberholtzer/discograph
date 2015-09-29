# -*- encoding: utf-8 -*-
import flask
import functools
import os
import random
import re
import redis
import time
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
from abjad.tools import systemtools
from werkzeug.contrib.cache import FileSystemCache


class DiscographAPI(object):

    urlify_pattern = re.compile(r"\s+", re.MULTILINE)

    ### INITIALIZER ###

    def __init__(self, app=None):
        import discograph
        config_path = os.path.join(discograph.__path__[0], 'discograph.cfg')
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
        self._app = app
        self._redis = redis.StrictRedis()
        self._cache = FileSystemCache(
            cache_path,
            default_timeout=60 * 60 * 48,
            threshold=1024 * 8,
            )
        print('Clearing cache.')
        self._cache.clear()

    ### PUBLIC METHODS ###

    def cache_get(self, cache_key):
        data = self.cache.get(cache_key)
        if data is not None:
            print('Cache Hit:  {}'.format(cache_key))
            data['cached'] = True
            return data
        print('Cache Miss: {}'.format(cache_key))

    def cache_set(self, cache_key, data):
        self.cache.set(cache_key, data)

    def get_artist(self, artist_id):
        import discograph
        query = discograph.SQLArtist.select()
        query = query.where(discograph.SQLArtist.id == artist_id)
        result = list(query)
        if not result:
            return None
        return result[0]

    def get_label(self, label_id):
        import discograph
        query = discograph.SQLLabel.select()
        query = query.where(discograph.SQLLabel.id == label_id)
        result = list(query)
        if not result:
            return None
        return result[0]

    def get_network(self, entity_type, entity_id, on_mobile=False, role_names=None, year=None):
        import discograph
        #cache_key = 'discograph:/api/{}/network/{}'.format(entity_type, entity_id)
        #if on_mobile:
        #    cache_key = '{}/mobile'.format(cache_key)
        #data = self.cache_get(cache_key)
        #if data is not None:
        #    return data
        if entity_type == 'artist':
            entity = self.get_artist(entity_id)
        elif entity_type == 'label':
            entity = self.get_label(entity_id)
        if entity is None:
            return None
        if not on_mobile:
            max_nodes = 75
            max_links = 150
            degree = 12
        else:
            max_nodes = 25
            max_links = 75
            degree = 6
        relation_grapher = discograph.RelationGrapher(
            center_entity=entity,
            degree=degree,
            max_nodes=max_nodes,
            max_links=max_links,
            role_names=role_names,
            year=year,
            )
        with systemtools.Timer(exit_message='Network query time:'):
            data = relation_grapher.get_network()
        #self.cache_set(cache_key, data)
        return data

    def get_random_entity(self, role_names=None):
        import discograph
        relation = discograph.SQLRelation.get_random(role_names=role_names)
        entity_choice = random.randint(1, 2)
        if entity_choice == 1:
            entity_type = relation.entity_one_type
            entity_id = relation.entity_one_id
        else:
            entity_type = relation.entity_two_type
            entity_id = relation.entity_two_id
        return entity_type, entity_id

    def limit(self, requests=10, window=60):
        def decorator(f):
            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                key = 'ratelimit:{}:{}'.format(
                    flask.request.endpoint,
                    flask.request.remote_addr,
                    )
                try:
                    remaining = requests - int(self.redis.get(key))
                except (ValueError, TypeError):
                    remaining = requests
                    self.redis.setex(key, window, 0)
                ttl = self.redis.ttl(key)
                if not ttl:
                    self.redis.expire(key, window)
                    ttl = window
                flask.g.view_limits = (requests, remaining - 1, time.time() + ttl)
                if 0 < remaining:
                    self.redis.incr(key, 1)
                    #print(key, remaining, ttl)
                    return f(*args, **kwargs)
                else:
                    #print(key, remaining, ttl)
                    return flask.Response('Too Many Requests', 429)
            return wrapped
        return decorator

    @staticmethod
    def parse_request_args(args):
        from discograph.library import ArtistRole
        year = None
        role_names = set()
        for key in args:
            if key == 'year':
                value = args[key]
                try:
                    if '-' in year:
                        start, _, stop = year.partition('-')
                        year = tuple(sorted((int(start), int(stop))))
                    else:
                        year = int(year)
                except:
                    pass
            elif key == 'roles[]':
                value = args.getlist(key)
                for role_name in value:
                    if role_name in ArtistRole._available_credit_roles:
                        role_names.add(role_name)
        role_names = list(sorted(role_names))
        return role_names, year

    def search_entities(self, search_string):
        import discograph
        cache_key = 'discograph:/api/search/{}'.format(
            self.urlify_pattern.sub('+', search_string))
        data = self.cache_get(cache_key)
        if data is not None:
            return data
        query = discograph.SQLFTSArtist.search_bm25(search_string).limit(10)
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
    def app(self):
        return self._app

    @property
    def application_url(self):
        return self._application_url

    @property
    def cache(self):
        return self._cache

    @property
    def redis(self):
        return self._redis