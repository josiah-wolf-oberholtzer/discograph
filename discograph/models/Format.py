import mongoengine
from discograph.models.Model import Model


class Format(Model, mongoengine.EmbeddedDocument):
    pass