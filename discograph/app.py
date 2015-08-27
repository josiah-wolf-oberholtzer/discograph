#! /usr/bin/env python
import traceback
from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    )
from werkzeug.contrib.cache import MemcachedCache


app = Flask(__name__)
cache = MemcachedCache(['127.0.0.1:11211'])


@app.route('/api/search/<name_fragment>', methods=['GET'])
@app.route('/api/search/<name_fragment>/', methods=['GET'])
def route__api__search__name_fragment(name_fragment):
    import discograph
    key = '/api/search/{}'.format(name_fragment).replace(' ', '-')
    data = cache.get(key)
    if data is not None:
        print('CACHE HIT:', key)
        return jsonify(data)
    print('CACHE MISS:', key)
    discograph.connect()
    query = discograph.models.Artist.objects(name__istartswith=name_fragment)
    query = query.only('discogs_id', 'name').limit(10)
    data = query.as_pymongo()
    data = tuple(data)
    data = {'items': data}
    cache.set(key, data, timeout=60 * 60)
    return jsonify(data)


@app.route('/api/cluster/<int:artist_id>', methods=['GET'])
@app.route('/api/cluster/<int:artist_id>/', methods=['GET'])
def route__api__cluster__artist_id(artist_id):
    import discograph
    key = '/api/cluster/{}'.format(artist_id)
    data = cache.get(key)
    if data is not None:
        print('CACHE HIT:', key)
        return jsonify(data)
    print('CACHE MISS:', key)
    discograph.connect()
    try:
        artist = discograph.models.Artist.objects.get(discogs_id=artist_id)
    except:
        abort(404)
    artist_graph = discograph.graphs.ArtistMembershipGrapher(
        [artist], 12)
    data = artist_graph.to_json(max_nodes=100)
    cache.set(key, data, timeout=60 * 60)
    return jsonify(data)


@app.route('/<int:artist_id>', methods=['GET'])
@app.route('/<int:artist_id>/', methods=['GET'])
def route__artist_id(artist_id):
    return render_template('index.html', artist_id=artist_id)


@app.route('/')
@app.route('/index')
@app.route('/index/')
def route():
    import discograph
    import random
    discograph.connect()
    count = discograph.models.Artist.objects.count()
    artist = None
    while artist is None:
        discogs_id = random.randrange(1, count)
        try:
            artist = discograph.models.Artist.objects.get(discogs_id=discogs_id)
        except:
            traceback.print_exc()
            artist = None
        if artist is None:
            continue
        if not artist.members and not artist.groups:
            artist = None
    artist_id = artist.discogs_id
    return redirect('/{}'.format(artist_id), code=302)


if __name__ == '__main__':
    app.run(debug=True)