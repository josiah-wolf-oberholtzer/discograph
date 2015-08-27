#! /usr/bin/env python
import traceback
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    )


app = Flask(__name__)


@app.route('/api/cluster/<int:artist_id>', methods=['GET'])
def route__api__cluster__artist_id(artist_id):
    import discograph
    discograph.connect()
    try:
        artist = discograph.models.Artist.objects.get(discogs_id=artist_id)
    except:
        abort(404)
    artist_graph = discograph.graphs.ArtistMembershipGrapher(
        [artist], 8)
    data = artist_graph.to_json(max_nodes=100)
    return jsonify(data)


@app.route('/api/cluster/random', methods=['GET'])
def route__api__cluster__random():
    import discograph
    import random
    discograph.connect()
    count = discograph.models.Artist.objects.count()
    artist = None
    while artist is None:
        discogs_id = random.randrange(1, count)
        print(discogs_id)
        try:
            artist = discograph.models.Artist.objects.get(discogs_id=discogs_id)
        except:
            traceback.print_exc()
            artist = None
        if artist is None:
            continue
        print(artist.name)
        if not artist.members and not artist.groups:
            artist = None
    artist_graph = discograph.graphs.ArtistMembershipGrapher(
        [artist], 8)
    data = artist_graph.to_json(max_nodes=100)
    return jsonify(data)


@app.route('/<int:artist_id>', methods=['GET'])
def route__artist_id(artist_id):
    return render_template('index.html')


@app.route('/')
@app.route('/index')
def route():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)