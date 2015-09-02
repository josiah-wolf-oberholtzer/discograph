import mongoengine
from discograph.models.Model import Model


class LabelReference(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    name = mongoengine.StringField()
    discogs_id = mongoengine.IntField()

    ### PUBLIC PROPERTIES ###

    @property
    def label(self):
        from discograph import models
        return models.Label.objects.get(discogs_id=self.discogs_id)