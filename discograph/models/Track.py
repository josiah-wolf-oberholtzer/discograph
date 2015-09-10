import mongoengine
from discograph import Bootstrapper
from discograph.models.ArtistCredit import ArtistCredit
from discograph.models.Model import Model


class Track(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    duration = mongoengine.StringField()
    extra_artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    position = mongoengine.StringField()
    title = mongoengine.StringField()

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        data = cls.tags_to_fields(element)
        document = cls(**data)
        return document


Track._tags_to_fields_mapping = {
    'artists': ('artists', ArtistCredit.from_elements),
    'duration': ('duration', Bootstrapper.element_to_string),
    'extraartists': ('extra_artists', ArtistCredit.from_elements),
    'position': ('position', Bootstrapper.element_to_string),
    'title': ('title', Bootstrapper.element_to_string),
    }