import mongoengine
from discograph.models.Model import Model


class Release(Model, mongoengine.Document):

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        pass