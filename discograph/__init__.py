import mongoengine
from discograph.Bootstrapper import Bootstrapper
from discograph.models import *
from discograph.app import app


def connect():
    return mongoengine.connect('discograph')


if __name__ == '__main__':
    app.run(debug=True)