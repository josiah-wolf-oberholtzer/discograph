#! /usr/bin/env python
import abjad
import discograph
import mongoengine
import re
from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    )
#from werkzeug.contrib.cache import MemcachedCache


app = Flask(__name__)
#cache = MemcachedCache(['127.0.0.1:11211'])
#cache.clear()
#cache = None
mongoengine.connect('discograph')


@app.route('/')
def route__index():
    return render_template(
        'index.html',
        artist=None,
        title='discoGraph',
        )


@app.route('/random')
def route__random():
    artist = discograph.library.SQLArtist.get_random()
    artist_id = artist.id
    return redirect('/artist/{}'.format(artist_id), code=302)


@app.route('/artist/<int:artist_id>', methods=['GET'])
def route__artist_id(artist_id):
    query = discograph.SQLArtist.select()
    query = query.where(discograph.SQLArtist.id == artist_id)
    result = list(query)
    if not result:
        abort(404)
    artist = result[0]
    return render_template(
        'index.html',
        key='artist-{}'.format(artist.id),
        title='discoGraph: {}'.format(artist.name),
        )


@app.route('/api/artist/network/<int:artist_id>', methods=['GET'])
def route__api__cluster(artist_id):
    try:
        artist = discograph.library.Artist.objects.get(discogs_id=artist_id)
    except:
        abort(404)
    role_names = [
        'Alias',
        'Member Of',
        #'Producer',
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
    relation_grapher = discograph.RelationGrapher(
        entities=[artist],
        degree=12,
        max_nodes=100,
        role_names=role_names,
        )
    with abjad.systemtools.Timer(exit_message='Network query time:'):
        data = relation_grapher.get_network()
    return jsonify(data)


urlify_pattern = re.compile(r"\s+", re.MULTILINE)


@app.route('/api/search/<search_string>', methods=['GET'])
def route__api__search(search_string):
    print(search_string)
    query = discograph.SQLFTSArtist.search_bm25(search_string).limit(10)
    data = []
    for sql_fts_artist in query:
        datum = dict(
            key='artist-{}'.format(sql_fts_artist.id),
            name=sql_fts_artist.name,
            )
        data.append(datum)
        print('    {}'.format(datum))
    data = {'results': tuple(data)}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)