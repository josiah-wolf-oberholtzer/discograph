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
        og_title='Disco/graph: visualizing music as a social graph',
        og_url='/',
        on_mobile=request.MOBILE,
        title='Disco/graph: Visualizing music as a social graph',
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
    title = 'Disco/graph: {}'.format(artist.name)
    rendered_template = render_template(
        'index.html',
        application_url=app.api.application_url,
        is_a_return_visitor=is_a_return_visitor,
        key=key,
        og_title='Disco/graph: The "{}" network'.format(artist.name),
        og_url=url,
        on_mobile=request.MOBILE,
        title=title,
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response


@app.route('/random')
def route__random():
    entity_type, entity_id = app.api.get_random_entity()
    if entity_type == 1:
        return redirect('/artist/{}'.format(entity_id), code=302)
    return redirect('/label/{}'.format(entity_id), code=302)


@app.route('/api/artist/network/<int:artist_id>', methods=['GET'])
@app.api.limit(requests=100, window=60)
def route__api__cluster(artist_id):
    on_mobile = request.MOBILE
    data = app.api.get_artist_network(artist_id, on_mobile=on_mobile)
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