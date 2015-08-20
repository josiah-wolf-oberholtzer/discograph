import mongoengine
from discograph.models.Model import Model


class Track(Model, mongoengine.EmbeddedDocument):
    pass