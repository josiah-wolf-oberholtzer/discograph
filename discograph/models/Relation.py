import mongoengine
from discograph.models.Model import Model
from discograph.models.Artist import Artist
from discograph.models.Label import Label
#from extras_mongoengine.fields import IntEnumField


class Relation(Model, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    entity_one = mongoengine.GenericReferenceField(choices=[Artist, Label])
    #entity_one_type = IntEnumField()
    entity_two = mongoengine.GenericReferenceField(choices=[Artist, Label])
    #entity_two_type = IntEnumField()
    release = mongoengine.ReferenceField('Release')
    role = mongoengine.StringField()
    #category = IntEnumField()
    #subcategory = IntEnumField()

    ### PUBLIC METHODS ###

    @staticmethod
    def from_release(release):
        artists = set(_.artist for _ in release.artists)
        labels = set(_.label for _ in release.labels)