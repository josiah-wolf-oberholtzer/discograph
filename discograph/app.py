#! /usr/bin/env python
# -*- encoding: utf-8 -*-
from flask import Flask
from flask import g
from flask import jsonify
from flask import make_response
from flask import render_template
from flask.ext.mobility import Mobility
from werkzeug.contrib.fixers import ProxyFix

from discograph import api
from discograph import ui
from discograph.library import DiscographAPI


discograph_api = DiscographAPI()

app = Flask(__name__)
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


@app.errorhandler(404)
def handler_404(error):
    rendered_template = render_template('404.html')
    response = make_response(rendered_template)
    return response


@app.errorhandler(500)
def handler_500(error):
    rendered_template = render_template('404.html')
    response = make_response(rendered_template)
    return response


@app.errorhandler(Exception)
def handle_error(error):
    print("FLAMINGO XXX")
    status_code = getattr(error, 'status_code', 400)
    response = jsonify({
        'success': False,
        'status': status_code,
        'message': getattr(error, 'message', 'Error')
        })
    response.status_code = status_code
    return response


if __name__ == '__main__':
    app.run(debug=True)