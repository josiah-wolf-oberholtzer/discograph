import mongoengine
from discograph.models.Model import Model


class ArtistReference(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    name = mongoengine.StringField()
    discogs_id = mongoengine.IntField()

    ### PUBLIC PROPERTIES ###

    @property
    def artist(self):
        from discograph import models
        return models.Artist.objects.get(discogs_id=self.discogs_id)