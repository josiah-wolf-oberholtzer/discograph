import mongoengine
from discograph import bootstrap
from discograph import graphs
from discograph import models


def connect():
    return mongoengine.connect('discograph')