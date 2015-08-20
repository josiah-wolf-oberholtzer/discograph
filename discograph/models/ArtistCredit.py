import mongoengine
from discograph.models.Model import Model


class ArtistCredit(Model, mongoengine.EmbeddedDocument):
    pass