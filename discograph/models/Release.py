import mongoengine
from discograph.models.Model import Model


class Release(Model, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    companies = mongoengine.EmbeddedDocumentListField('CompanyCredit')
    country = mongoengine.StringField()
    data_quality = mongoengine.StringField()
    extra_artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    formats = mongoengine.EmbeddedDocumentListField('Format')
    genres = mongoengine.ListField(mongoengine.StringField())
    identifiers = mongoengine.EmbeddedDocumentListField('Identifier')
    labels = mongoengine.EmbeddedDocumentListField('LabelCredit')
    master_id = mongoengine.IntField()
    notes = mongoengine.StringField()
    release_date = mongoengine.DateTimeField()
    styles = mongoengine.ListField(mongoengine.StringField())
    title = mongoengine.StringField()
    tracklist = mongoengine.EmbeddedDocumentListField('Track')

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        from discograph import models
        # artists
        artists = element.find('artists')
        if artists is not None and len(artists):
            artists = [models.ArtistCredit.from_element(_) for _ in artists]
        else:
            artists = None
        # companies
        # country
        country = element.find('country').text
        # data quality
        data_quality = element.find('data_quality').text
        # extra artists
        extra_artists = element.find('extraartists')
        if extra_artists is not None and len(extra_artists):
            extra_artists = [models.ArtistCredit.from_element(_) for _ in extra_artists]
        else:
            extra_artists = None
        # formats
        formats = element.find('formats')
        if formats is not None and len(formats):
            formats = [models.Format.from_element(_) for _ in formats]
        else:
            formats = None
        # genres
        genres = element.find('genres')
        if genres is not None and len(genres):
            genres = [_.text for _ in genres]
        else:
            genres = None
        # identifiers
        identifiers = element.find('identifiers')
        if identifiers is not None and len(identifiers):
            identifiers = [models.Identifier.from_element(_) for _ in identifiers]
        else:
            identifiers = None
        # labels
        # master_id
        # notes
        # release_date
        # styles
        styles = element.find('styles')
        if styles is not None and len(styles):
            styles = [_.text for _ in styles]
        else:
            styles = None
        # title
        title = element.find('title').text
        # tracklist
        # construct
        release_document = cls(
            artists=artists,
            country=country,
            data_quality=data_quality,
            extra_artists=extra_artists,
            formats=formats,
            genres=genres,
            identifiers=identifiers,
            styles=styles,
            title=title,
            )
        return release_document