#! /usr/bin/env python
# -*- encoding: utf-8 -*-
from flask import Flask, g
from flask.ext.mobility import Mobility
from werkzeug.contrib.fixers import ProxyFix
from discograph.endpoints import endpoints


app = Flask(__name__)
app.register_blueprint(endpoints)
app.debug = True
app.wsgi_app = ProxyFix(app.wsgi_app)
Mobility(app)


@app.after_request
def inject_rate_limit_headers(response):
    try:
        requests, remaining, reset = map(int, g.view_limits)
    except (AttributeError, ValueError):
        return response
    else:
        h = response.headers
        h.add('X-RateLimit-Remaining', remaining)
        h.add('X-RateLimit-Limit', requests)
        h.add('X-RateLimit-Reset', reset)
        return response


if __name__ == '__main__':
    app.run(debug=True)