#! /usr/bin/env python
import discograph
import mongoengine
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
cache.clear()
mongoengine.connect('discograph')


@app.route('/')
@app.route('/index')
@app.route('/index/')
def route():
    import random
    count = discograph.models.Artist.objects.count()
    artist = None
    while artist is None:
        discogs_id = random.randrange(1, count)
        try:
            artist = discograph.models.Artist.objects.get(
                discogs_id=discogs_id)
        except:
            traceback.print_exc()
            artist = None
        if artist is None:
            continue
        if not artist.members and not artist.groups:
            artist = None
    artist_id = artist.discogs_id
    return redirect('/{}'.format(artist_id), code=302)


@app.route('/<int:artist_id>', methods=['GET'])
@app.route('/<int:artist_id>/', methods=['GET'])
def route__artist_id(artist_id):
    try:
        artist = discograph.models.Artist.objects.get(discogs_id=artist_id)
    except:
        abort(404)
    return render_template('index.html', artist=artist)


@app.route('/api/artist/network/<int:artist_id>', methods=['GET'])
@app.route('/api/artist/network/<int:artist_id>/', methods=['GET'])
def route__api__cluster__artist_id(artist_id):
    key = 'cache:/api/artist/network/{}'.format(artist_id)
    data = cache.get(key)
    if data is not None:
        #print('CACHE HIT:', key)
        return jsonify(data)
    #print('CACHE MISS:', key)
    try:
        artist = discograph.models.Artist.objects.get(discogs_id=artist_id)
    except:
        abort(404)
    artist_graph = discograph.graphs.ArtistMembershipGrapher(
        artists=[artist],
        cache=cache,
        degree=12,
        max_nodes=100,
        )
    data = artist_graph.get_network()
    cache.set(key, data)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)