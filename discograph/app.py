#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import traceback

from flask import Flask
from flask import g
from flask import jsonify
from flask import make_response
from flask import render_template
from flask import request
from flask.ext.mobility import Mobility
from werkzeug.contrib.cache import FileSystemCache
from werkzeug.contrib.fixers import ProxyFix

from discograph import api
from discograph import ui
from discograph import exceptions


app = Flask(__name__)
app.config.from_object('discograph.config.DevelopmentConfiguration')
app.cache = FileSystemCache(
    app.config['FILE_CACHE_PATH'],
    default_timeout=app.config['FILE_CACHE_TIMEOUT'],
    threshold=app.config['FILE_CACHE_THRESHOLD'],
    )
if not os.path.exists(app.config['FILE_CACHE_PATH']):
    os.makedirs(app.config['FILE_CACHE_PATH'])
app.register_blueprint(api.blueprint, url_prefix='/api')
app.register_blueprint(ui.blueprint)
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


@app.errorhandler(Exception)
def handle_error(error):
    if app.debug:
        traceback.print_exc()
    status_code = getattr(error, 'status_code', 400)
    if request.endpoint.startswith('api'):
        response = jsonify({
            'success': False,
            'status': status_code,
            'message': getattr(error, 'message', 'Error')
            })
    else:
        rendered_template = render_template('error.html', error=error)
        response = make_response(rendered_template)
    response.status_code = status_code
    return response


@app.errorhandler(404)
def handle_error_404(error):
    status_code = 404
    error = exceptions.APIError(
        message='Not Found',
        status_code=status_code,
        )
    rendered_template = render_template('error.html', error=error)
    response = make_response(rendered_template)
    response.status_code = status_code
    return response


@app.errorhandler(500)
def handle_error_500(error):
    status_code = 500
    error = exceptions.APIError(
        message='Something Broke',
        status_code=status_code,
        )
    rendered_template = render_template('error.html', error=error)
    response = make_response(rendered_template)
    response.status_code = status_code
    return response


if __name__ == '__main__':
    app.run(debug=True)