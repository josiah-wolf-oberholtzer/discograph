import mongoengine
from discograph.bootstrap import Bootstrap
from discograph.models.Model import Model


class ArtistCredit(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    anv = mongoengine.StringField()
    artist = mongoengine.ReferenceField('Artist')
    join = mongoengine.StringField()
    roles = mongoengine.ListField(mongoengine.StringField())
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

    @classmethod
    def element_to_roles(cls, element):
        if element is not None and element.text:
            return cls.parse_roles(element.text)
        return []

    @classmethod
    def parse_roles(cls, text):
        roles = []
        role = ''
        in_bracket = False
        for c in text:
            if not in_bracket and c == '[':
                in_bracket = True
            elif in_bracket and c == ']':
                in_bracket = False
            elif not in_bracket and c == ',':
                role = role.strip()
                if role:
                    roles.append(role)
                role = ''
                continue
            role += c
        role = role.strip()
        if role:
            roles.append(role)
        return roles


ArtistCredit._tags_to_fields_mapping = {
    'anv': ('anv', Bootstrap.element_to_string),
    'id': ('discogs_id', Bootstrap.element_to_integer),
    'join': ('join', Bootstrap.element_to_string),
    'name': ('name', Bootstrap.element_to_string),
    'role': ('roles', ArtistCredit.element_to_roles),
    'tracks': ('tracks', Bootstrap.element_to_string),
    }