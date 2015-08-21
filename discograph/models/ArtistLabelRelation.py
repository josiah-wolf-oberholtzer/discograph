import mongoengine
from discograph.models.Model import Model


class ArtistLabelRelation(Model, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    artist = mongoengine.ReferenceField('Artist')
    label = mongoengine.ReferenceField('Label')
    release = mongoengine.ReferenceField('Release')

    ### MONGOENGINE META ###

    meta = {
        'collection': 'relations',
        }