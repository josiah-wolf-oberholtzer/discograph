# -*- encoding: utf-8 -*-
import flask
import functools
import re
import redis
import time

from discograph import exceptions


redis_client = redis.StrictRedis()


class cache(object):

    urlify_pattern = re.compile(r"\s+", re.MULTILINE)

    def __init__(self, cache_key):
        from discograph import app
        self.cache_object = app.cache
        self.cache_key = cache_key

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped


def limit(max_requests=10, period=60):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):

            # For testing error handlers:
            # max_requests = 2

            key = 'ratelimit:{}:{}'.format(
                flask.request.endpoint,
                flask.request.remote_addr,
                )

            try:
                remaining = max_requests - int(redis_client.get(key))
            except (ValueError, TypeError):
                remaining = max_requests
                redis_client.setex(key, period, 0)

            ttl = redis_client.ttl(key)
            if not ttl:
                redis_client.expire(key, period)
                ttl = period

            flask.g.view_limits = (max_requests, remaining - 1, time.time() + ttl)

            if 0 < remaining:
                redis_client.incr(key, 1)
                print(key, remaining, ttl)
                return f(*args, **kwargs)
            else:
                print(key, remaining, ttl)
                raise exceptions.RateLimitError()

        return wrapped
    return decorator


__all__ = ['cache', 'limit']