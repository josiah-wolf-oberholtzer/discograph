#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import discograph
from flask import Flask, g
from flask.ext.mobility import Mobility
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)
app.debug = True
app.api = discograph.library.DiscographAPI(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
Mobility(app)


import endpoints


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