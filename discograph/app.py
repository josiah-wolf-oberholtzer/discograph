#! /usr/bin/env python
import discograph
from flask import Flask, abort, jsonify, make_response, redirect, render_template, request, g
from flask.ext.mobility import Mobility


app = Flask(__name__)
app.debug = True
app.api = discograph.DiscographAPI(app)
Mobility(app)


@app.route('/')
def route__index():
    is_a_return_visitor = request.cookies.get('is_a_return_visitor')
    rendered_template = render_template(
        'index.html',
        artist=None,
        application_url=app.api.application_url,
        is_a_return_visitor=is_a_return_visitor,
        og_title='Discograph: visualizing music as a social graph',
        og_url='/',
        on_mobile=request.MOBILE,
        title='discograph: Visualizing music as a social graph',
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response


@app.route('/artist/<int:artist_id>', methods=['GET'])
def route__artist_id(artist_id):
    artist = app.api.get_artist(artist_id)
    if artist is None:
        abort(404)
    is_a_return_visitor = request.cookies.get('is_a_return_visitor')
    key = 'artist-{}'.format(artist.id)
    url = '/artist/{}'.format(artist.id)
    title = 'discograph: {}'.format(artist.name)
    rendered_template = render_template(
        'index.html',
        application_url=app.api.application_url,
        is_a_return_visitor=is_a_return_visitor,
        key=key,
        og_title='Discograph: The "{}" network'.format(artist.name),
        og_url=url,
        on_mobile=request.MOBILE,
        title=title,
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response


@app.route('/label/<int:label_id>', methods=['GET'])
def route__label_id(label_id):
    label = app.api.get_label(label_id)
    if label is None:
        abort(404)
    is_a_return_visitor = request.cookies.get('is_a_return_visitor')
    key = 'label-{}'.format(label.id)
    url = '/label/{}'.format(label.id)
    title = 'discograph: {}'.format(label.name)
    rendered_template = render_template(
        'index.html',
        application_url=app.api.application_url,
        is_a_return_visitor=is_a_return_visitor,
        key=key,
        og_title='Discograph: The "{}" network'.format(label.name),
        og_url=url,
        on_mobile=request.MOBILE,
        title=title,
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response


@app.route('/random')
def route__random():
    role_names, year = app.api.parse_request_args(request.args)
    if not role_names:
        role_names = [
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
    entity_type, entity_id = app.api.get_random_entity(role_names)
    if entity_type == 1:
        return redirect('/artist/{}'.format(entity_id), code=302)
    return redirect('/label/{}'.format(entity_id), code=302)


@app.route('/api/<entity_type>/network/<int:entity_id>', methods=['GET'])
@app.api.limit(requests=100, window=60)
def route__api__network(entity_type, entity_id):
    if entity_type not in ('artist', 'label'):
        abort(404)
    role_names, year = app.api.parse_request_args(request.args)
    if not role_names:
        role_names = [
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
@app.api.limit(requests=200, window=60)
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