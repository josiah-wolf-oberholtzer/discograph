import mongoengine
from discograph.models.Model import Model
from discograph.models.Artist import Artist
from discograph.models.Label import Label
from extras_mongoengine.fields import IntEnumField


class ArtistArtistRelation(Model, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    entity_one = mongoengine.GenericReferenceField(choices=[Artist, Label])
    entity_one_type = IntEnumField()
    entity_two = mongoengine.GenericReferenceField(choices=[Artist, Label])
    entity_two_type = IntEnumField()
    release = mongoengine.ReferenceField('Release')
    role = IntEnumField()