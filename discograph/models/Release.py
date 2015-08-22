from __future__ import print_function
import datetime
import gzip
import mongoengine
import re
from discograph.models.Model import Model


class Release(Model, mongoengine.Document):

    ### CLASS VARIABLES ###

    date_regex = re.compile('^(\d{4})-(\d{2})-(\d{2})$')
    date_no_dashes_regex = re.compile('^(\d{4})(\d{2})(\d{2})$')
    year_regex = re.compile('^\d\d\d\d$')

    ### MONGOENGINE FIELDS ###

    artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    companies = mongoengine.EmbeddedDocumentListField('CompanyCredit')
    country = mongoengine.StringField()
    data_quality = mongoengine.StringField()
    discogs_id = mongoengine.IntField(required=True, unique=True)
    extra_artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    formats = mongoengine.EmbeddedDocumentListField('Format')
    genres = mongoengine.ListField(mongoengine.StringField())
    identifiers = mongoengine.EmbeddedDocumentListField('Identifier')
    labels = mongoengine.EmbeddedDocumentListField('LabelCredit')
    master_id = mongoengine.IntField()
    release_date = mongoengine.DateTimeField()
    status = mongoengine.StringField()
    styles = mongoengine.ListField(mongoengine.StringField())
    title = mongoengine.StringField()
    tracklist = mongoengine.EmbeddedDocumentListField('Track')

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        from discograph import bootstrap
        cls.drop_collection()
        releases_xml_path = bootstrap.releases_xml_path
        with gzip.GzipFile(releases_xml_path, 'r') as file_pointer:
            releases_iterator = bootstrap.iterparse(file_pointer, 'release')
            releases_iterator = bootstrap.clean_elements(releases_iterator)
            for release_element in releases_iterator:
                release_document = cls.from_element(release_element)
                print(u'RELEASE {}: {}'.format(
                    release_document.discogs_id,
                    release_document.title,
                    ))

    def extract_relations(self):
        result = []
        return result

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
        country = element.find('country')
        if country is not None:
            country = country.text
        # data quality
        data_quality = element.find('data_quality').text
        # discogs id
        discogs_id = int(element.attrib.get('id'))
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
            release_date = cls.parse_release_date(release_date.text)
        # status
        status = element.attrib.get('status')
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
            discogs_id=discogs_id,
            extra_artists=extra_artists,
            formats=formats,
            genres=genres,
            identifiers=identifiers,
            labels=labels,
            master_id=master_id,
            release_date=release_date,
            status=status,
            styles=styles,
            title=title,
            tracklist=tracklist,
            )
        release_document.save()
        return release_document

    @classmethod
    def parse_release_date(cls, release_date):
        release_date = release_date.strip()
        # empty string
        if not release_date:
            return None
        # yyyy-mm-dd
        match = cls.date_regex.match(release_date)
        if match:
            year, month, day = match.groups()
            return cls.validate_release_date(year, month, day)
        # yyyy
        match = cls.date_no_dashes_regex.match(release_date)
        if match:
            year, month, day = match.group(), 1, 1
            return cls.validate_release_date(year, month, day)
        # yyyymmdd
        match = cls.date_no_dashes_regex.match(release_date)
        if match:
            year, month, day = match.groups()
            return cls.validate_release_date(year, month, day)
        # other: "?", "????", "None", "Unknown"
        return None

    @classmethod
    def validate_release_date(cls, year, month, day):
        year = int(year)
        if month.isdigit():
            month = int(month) or 1
        else:
            month = 1
        if day.isdigit():
            day = int(day) or 1
        else:
            day = 1
        date = datetime.datetime(year, month, 1)
        date = date + datetime.timedelta(days=day - 1)
        return date