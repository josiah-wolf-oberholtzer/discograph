from discograph.library import *
from discograph.DiscographAPI import DiscographAPI
from discograph.app import app


def connect():
    import mongoengine
    return mongoengine.connect('discograph')


if __name__ == '__main__':
    app.run(debug=True)