import mongoengine
from discograph.models.Model import Model


class ArtistArtistRelation(Model, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    artist_one = mongoengine.ReferenceField('Artist')
    artist_two = mongoengine.ReferenceField('Artist')
    role = mongoengine.StringField()
    release = mongoengine.ReferenceField('Release')

    ### MONGOENGINE META ###

    meta = {
        'collection': 'relations',
        }