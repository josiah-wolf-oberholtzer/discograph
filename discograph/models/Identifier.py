import mongoengine
from discograph.models.Model import Model


class Identifier(Model, mongoengine.EmbeddedDocument):
    pass