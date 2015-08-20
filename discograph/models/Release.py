import mongoengine
from discograph.models.Model import Model


class Release(Model, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    title = mongoengine.StringField()
    labels = mongoengine.EmbeddedDocumentListField('LabelCredit')
    extra_artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    formats = mongoengine.EmbeddedDocumentListField('Format')
    genres = mongoengine.ListField(mongoengine.StringField())
    styles = mongoengine.ListField(mongoengine.StringField())
    country = mongoengine.StringField()
    released = mongoengine.DateTimeField()
    # notes = mongoengine.StringField()
    master_id = mongoengine.IntField()
    # data_quality = mongoengine.StringField()
    tracklist = mongoengine.EmbeddedDocumentListField('Track')
    identifier = mongoengine.EmbeddedDocumentListField('Identifier')
    companies = mongoengine.EmbeddedDocumentListField('CompanyCredit')

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        from discograph import models
        artists = element.find('artists')
        if artists is not None and len(artists):
            artists = [models.ArtistCredit.from_element(_) for _ in artists]
        else:
            artists = []
        extra_artists = element.find('extraartists')
        if extra_artists is not None and len(extra_artists):
            extra_artists = [models.ArtistCredit.from_element(_) for _ in extra_artists]
        else:
            extra_artists = []
        release_document = cls(
            artists=artists,
            extra_artists=extra_artists,
            )
        return release_document