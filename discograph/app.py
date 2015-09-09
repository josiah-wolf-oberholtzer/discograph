#! /usr/bin/env python
import Levenshtein
import discograph
import mongoengine
import random
import re
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
def route__index():
    return render_template(
        'index.html',
        artist=None,
        title='discoGraph',
        )


@app.route('/random')
@app.route('/random/')
def route__random():
    count = discograph.models.Artist.objects.count()
    index = random.randrange(count)
    artist = discograph.models.Artist.objects[index]
    while not artist.members and not artist.groups:
        index = random.randrange(count)
        artist = discograph.models.Artist.objects[index]
    artist_id = artist.discogs_id
    return redirect('/artist/{}'.format(artist_id), code=302)


@app.route('/artist/<int:artist_id>', methods=['GET'])
@app.route('/artist/<int:artist_id>/', methods=['GET'])
def route__artist_id(artist_id):
    try:
        artist = discograph.models.Artist.objects.get(discogs_id=artist_id)
    except:
        abort(404)
    return render_template(
        'index.html',
        key='artist-{}'.format(artist.discogs_id),
        title='discoGraph: {}'.format(artist.name),
        )


@app.route('/api/artist/network/<int:artist_id>', methods=['GET'])
@app.route('/api/artist/network/<int:artist_id>/', methods=['GET'])
def route__api__cluster(artist_id):
    key = 'cache:/api/artist/network/{}'.format(artist_id)
    data = cache.get(key)
    if data is not None:
        print('NETWORK CACHE HIT:', key)
        return jsonify(data)
    print('NETWORK CACHE MISS:', key)
    try:
        artist = discograph.models.Artist.objects.get(discogs_id=artist_id)
    except:
        abort(404)
    relation_grapher = discograph.graphs.RelationGrapher2(
        entities=[artist],
        cache=cache,
        degree=12,
        max_nodes=200,
        )
    data = relation_grapher.get_network()
    cache.set(key, data)
    return jsonify(data)


urlify_pattern = re.compile(r"\s+", re.MULTILINE)


@app.route('/api/search/<search_string>', methods=['GET'])
def route__api__search(search_string):
    key = 'cache:/api/search/{}'.format(search_string)
    key = urlify_pattern.sub('+', key)
    print(key)
    data = cache.get(key)
    if data is not None:
        #print('CACHE HIT:', key)
        return jsonify(data)
    #print('CACHE MISS:', key)
    data = discograph.models.Artist.search_text(search_string, limit=50)
    data.sort(key=lambda x: Levenshtein.distance(x['name'], search_string))
    print(search_string)
    for datum in data:
        datum['key'] = 'artist-{}'.format(datum['_id'])
        del(datum['_id'])
        print(datum)
    data = {'results': data}
    cache.set(key, data)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)