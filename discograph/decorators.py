# -*- encoding: utf-8 -*-
import flask
import functools
import redis
import time

import exceptions


redis_client = redis.StrictRedis()


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