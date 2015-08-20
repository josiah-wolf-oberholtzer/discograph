import mongoengine
from discograph.models.Model import Model


class CompanyCredit(Model, mongoengine.EmbeddedDocument):
    pass