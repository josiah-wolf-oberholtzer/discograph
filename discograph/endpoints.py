# -*- encoding: utf-8 -*-
import json
from flask import Blueprint
from flask import make_response
from flask import redirect
from flask import request
from flask import jsonify
from flask import render_template
from flask import abort

from discograph import decorators
from discograph import exceptions
from discograph.library import DiscographAPI


api = DiscographAPI()
endpoints = Blueprint('endpoints', __name__, template_folder='templates')


@endpoints.route('/')
def route__index():
    is_a_return_visitor = request.cookies.get('is_a_return_visitor')
    initial_json = 'var dgData = null;'
    rendered_template = render_template(
        'index.html',
        artist=None,
        application_url=api.application_url,
        initial_json=initial_json,
        is_a_return_visitor=is_a_return_visitor,
        og_title='Disco/graph: visualizing music as a social graph',
        og_url='/',
        on_mobile=request.MOBILE,
        title='Disco/graph: Visualizing music as a social graph',
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response


@endpoints.route('/artist/<int:artist_id>')
def route__artist_id(artist_id):
    on_mobile = request.MOBILE
    data = api.get_artist_network(artist_id, on_mobile=on_mobile)
    if data is None:
        abort(404)
    initial_json = json.dumps(
        data,
        sort_keys=True,
        indent=4,
        separators=(',', ': '),
        )
    initial_json = 'var dgData = {};'.format(initial_json)
    is_a_return_visitor = request.cookies.get('is_a_return_visitor')
    artist = api.get_artist(artist_id)
    key = 'artist-{}'.format(artist.id)
    url = '/artist/{}'.format(artist.id)
    title = 'Disco/graph: {}'.format(artist.name)
    rendered_template = render_template(
        'index.html',
        application_url=api.application_url,
        initial_json=initial_json,
        is_a_return_visitor=is_a_return_visitor,
        key=key,
        og_title='Disco/graph: The "{}" network'.format(artist.name),
        og_url=url,
        on_mobile=on_mobile,
        title=title,
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response


@endpoints.route('/random')
def route__random():
    entity_type, entity_id = api.get_random_entity()
    if entity_type == 1:
        return redirect('/artist/{}'.format(entity_id), code=302)
    return redirect('/label/{}'.format(entity_id), code=302)


@endpoints.route('/api/random')
@decorators.limit(max_requests=60, period=60)
def route__api__random():
    role_names = ['Alias', 'Member Of']
    entity_type, entity_id = api.get_random_entity(role_names=role_names)
    entity_type = {
        1: 'artist',
        2: 'label',
        }[entity_type]
    data = {'center': '{}-{}'.format(entity_type, entity_id)}
    return jsonify(data)


@endpoints.route('/api/artist/network/<int:artist_id>')
@decorators.limit(max_requests=60, period=60)
def route__api__artist__network__artist_id(artist_id):
    on_mobile = request.MOBILE
    data = api.get_artist_network(artist_id, on_mobile=on_mobile)
    if data is None:
        abort(404)
    return jsonify(data)


@endpoints.route('/api/search/<search_string>')
@decorators.limit(max_requests=120, period=60)
def route__api__search(search_string):
    data = api.search_entities(search_string)
    return jsonify(data)


@endpoints.route('/api/ping')
@decorators.limit(max_requests=200, period=60)
def route__api__ping():
    print('PING', request.remote_addr)
    return jsonify({'ping': True})


@endpoints.errorhandler(exceptions.RateLimitError)
def handle_rate_limit_error(error):
    response = jsonify({
        'type': 'client',
        'message': error.message,
        'resource': error.resource})
    response.status_code = error.status_code or 429
    return response


@endpoints.errorhandler(exceptions.APIError)
def handle_api_error(error):
    response = jsonify({
        'type': 'client',
        'message': error.message,
        'resource': error.resource,
        'field': error.field})
    response.status_code = error.status_code or 400
    return response