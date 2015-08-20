import mongoengine
from discograph.models.Model import Model


class ArtistCredit(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    artist = mongoengine.ReferenceField('Artist')
    anv = mongoengine.StringField()
    join = mongoengine.StringField()
    role = mongoengine.StringField()
    tracks = mongoengine.StringField()

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        from discograph import models
        artist_discogs_id = int(element.find('id').text)
        artist_name = element.find('name').text
        artist = models.Artist.from_id_and_name(artist_discogs_id, artist_name)
        anv = element.find('anv').text or None
        join = element.find('join').text or None
        role = element.find('role').text or None
        tracks = element.find('tracks').text or None
        artist_credit_document = cls(
            artist=artist,
            anv=anv,
            join=join,
            role=role,
            tracks=tracks,
            )
        return artist_credit_document