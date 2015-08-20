import mongoengine
from discograph.models.Model import Model


class LabelCredit(Model, mongoengine.EmbeddedDocument):
    pass