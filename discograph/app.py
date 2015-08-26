#! /usr/bin/env python
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
    artist_graph = discograph.graphs.ArtistMembershipGrapher([artist], 3)
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