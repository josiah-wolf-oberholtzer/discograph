import mongoengine
from discograph.bootstrap import Bootstrap
from discograph.models.Model import Model


class ArtistCredit(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    anv = mongoengine.StringField()
    artist = mongoengine.ReferenceField('Artist')
    join = mongoengine.StringField()
    role = mongoengine.StringField()
    tracks = mongoengine.StringField()

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        from discograph import models
        data = cls.tags_to_fields(element)
        name = data['name']
        discogs_id = data['discogs_id']
        del(data['name'])
        del(data['discogs_id'])
        data['artist'] = models.Artist.from_id_and_name(discogs_id, name)
        document = cls(**data)
        return document


ArtistCredit._tags_to_fields_mapping = {
    'anv': ('anv', Bootstrap.element_to_string),
    'id': ('discogs_id', Bootstrap.element_to_integer),
    'join': ('join', Bootstrap.element_to_string),
    'name': ('name', Bootstrap.element_to_string),
    'role': ('role', Bootstrap.element_to_string),
    'tracks': ('tracks', Bootstrap.element_to_string),
    }