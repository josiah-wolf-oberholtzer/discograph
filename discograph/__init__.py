import mongoengine
from discograph.Bootstrapper import Bootstrapper
from discograph.RelationGrapher import RelationGrapher
from discograph.models import *


def connect():
    return mongoengine.connect('discograph')