#! /usr/bin/env python
import discograph
from flask import Flask, abort, jsonify, make_response, redirect, render_template, request, g
from flask.ext.mobility import Mobility


app = Flask(__name__)
app.debug = True
app.api = discograph.DiscographAPI(app)
Mobility(app)


default_role_names = [
    'Alias',
    'Member Of',
    #'Released On',
    #'Sublabel Of',
    #'Producer',
    #'Remix',
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


@app.route('/')
def route__index():
    is_a_return_visitor = request.cookies.get('is_a_return_visitor')
    multiselect_mapping = discograph.ArtistRole.get_multiselect_mapping()
    rendered_template = render_template(
        'index.html',
        artist=None,
        application_url=app.api.application_url,
        is_a_return_visitor=is_a_return_visitor,
        multiselect_mapping=multiselect_mapping,
        og_title='Disco/graph: visualizing music as a social graph',
        og_url='/',
        on_mobile=request.MOBILE,
        title='Disco/graph: Visualizing music as a social graph',
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response


@app.route('/<entity_type>/<int:entity_id>', methods=['GET'])
def route__entity(entity_type, entity_id):
    if entity_type not in ('artist', 'label'):
        abort(404)
    if entity_type == 'artist':
        entity = app.api.get_artist(entity_id)
    else:
        entity = app.api.get_label(entity_id)
    if entity is None:
        abort(404)
    original_role_names, original_year = app.api.parse_request_args(
        request.args)
    is_a_return_visitor = request.cookies.get('is_a_return_visitor')
    key = '{}-{}'.format(entity_type, entity.id)
    url = '/{}/{}'.format(entity_type, entity.id)
    title = 'Disco/graph: {}'.format(entity.name)
    multiselect_mapping = discograph.ArtistRole.get_multiselect_mapping()
    rendered_template = render_template(
        'index.html',
        application_url=app.api.application_url,
        is_a_return_visitor=is_a_return_visitor,
        key=key,
        multiselect_mapping=multiselect_mapping,
        og_title='Disco/graph: The "{}" network'.format(entity.name),
        og_url=url,
        on_mobile=request.MOBILE,
        original_role_names=original_role_names,
        title=title,
        original_year=original_year,
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response


@app.route('/random')
def route__random():
    role_names, year = app.api.parse_request_args(request.args)
    role_names = role_names or default_role_names[:]
    entity_type, entity_id = app.api.get_random_entity(role_names)
    if entity_type == 1:
        return redirect('/artist/{}'.format(entity_id), code=302)
    return redirect('/label/{}'.format(entity_id), code=302)


@app.route('/api/<entity_type>/network/<int:entity_id>', methods=['GET'])
#@app.api.limit(requests=100, window=60)
def route__api__network(entity_type, entity_id):
    if entity_type not in ('artist', 'label'):
        abort(404)
    role_names, year = app.api.parse_request_args(request.args)
    print('NETWORK SEARCH:', entity_type, entity_id)
    print('ROLES:         ', role_names)
    print('YEAR:          ', year)
    role_names = role_names or default_role_names[:]
    role_names = set(role_names)
    role_names.add('Member Of')
    role_names.add('Alias')
    role_names = sorted(role_names)
    on_mobile = request.MOBILE
    data = app.api.get_network(
        entity_type,
        entity_id,
        on_mobile=on_mobile,
        role_names=role_names,
        )
    if data is None:
        abort(404)
    return jsonify(data)


@app.route('/api/search/<search_string>', methods=['GET'])
#@app.api.limit(requests=200, window=60)
def route__api__search(search_string):
    data = app.api.search_entities(search_string)
    return jsonify(data)


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