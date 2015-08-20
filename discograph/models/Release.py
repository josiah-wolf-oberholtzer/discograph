import datetime
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
        companies = element.find('companies')
        if companies is not None and len(companies):
            companies = [models.CompanyCredit.from_element(_) for _ in companies]
        else:
            companies = None
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
        labels = element.find('labels')
        if labels is not None and len(labels):
            labels = [models.LabelCredit.from_element(_) for _ in labels]
        else:
            labels = None
        # master_id
        master_id = element.find('master_id')
        if master_id is not None:
            master_id = int(master_id.text)
        # release_date
        release_date = element.find('released')
        if release_date is not None:
            release_date = release_date.text
            release_date = datetime.datetime.strptime(release_date, '%Y-%m-%d')
        # styles
        styles = element.find('styles')
        if styles is not None and len(styles):
            styles = [_.text for _ in styles]
        else:
            styles = None
        # title
        title = element.find('title').text
        # tracklist
        tracklist = element.find('tracklist')
        if tracklist is not None and len(tracklist):
            tracklist = [models.Track.from_element(_) for _ in tracklist]
        else:
            tracklist = None
        # construct
        release_document = cls(
            artists=artists,
            companies=companies,
            country=country,
            data_quality=data_quality,
            extra_artists=extra_artists,
            formats=formats,
            genres=genres,
            identifiers=identifiers,
            labels=labels,
            master_id=master_id,
            release_date=release_date,
            styles=styles,
            title=title,
            tracklist=tracklist,
            )
        return release_document