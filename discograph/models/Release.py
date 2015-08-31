from __future__ import print_function
import datetime
import gzip
import mongoengine
import re
import traceback
from abjad.tools import systemtools
from discograph.bootstrap import Bootstrap
from discograph.models.ArtistCredit import ArtistCredit
from discograph.models.CompanyCredit import CompanyCredit
from discograph.models.Format import Format
from discograph.models.Identifier import Identifier
from discograph.models.LabelCredit import LabelCredit
from discograph.models.Model import Model
from discograph.models.Track import Track


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

    ### MONGOENGINE META ###

    meta = {
        'indexes': [
            'discogs_id',
            'title',
            '$title',
            ],
        'ordering': ['+discogs_id'],
        }

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        #cls.drop_collection()
        releases_xml_path = Bootstrap.releases_xml_path
        with gzip.GzipFile(releases_xml_path, 'r') as file_pointer:
            releases_iterator = Bootstrap.iterparse(file_pointer, 'release')
            releases_iterator = Bootstrap.clean_elements(releases_iterator)
            for release_element in releases_iterator:
                cls.from_element(release_element)

    @classmethod
    def from_element(cls, element):
        index = [('discogs_id', 1)]
        discogs_id = int(element.attrib.get('id'))
        query_set = cls.objects(discogs_id=discogs_id)\
            .hint(index)\
            .only('discogs_id', 'title')
            #.no_dereference()
        if 0 < query_set.count():
            document = query_set[0]
            message = u'RELEASE {} [preserved]: {}'.format(
                document.discogs_id,
                document.title,
                )
            print(message)
            return document
        with systemtools.Timer(verbose=False) as timer:
            data = cls.tags_to_fields(element)
            data.update(
                discogs_id=discogs_id,
                status=element.attrib.get('status'),
                )
            document = cls(**data)
            document.save()
        message = u'RELEASE {} [{}]: {}'.format(
            document.discogs_id,
            timer.elapsed_time,
            document.title,
            )
        print(message)
        return document

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
        # yyyymmdd
        match = cls.date_no_dashes_regex.match(release_date)
        if match:
            year, month, day = match.groups()
            return cls.validate_release_date(year, month, day)
        # yyyy
        match = cls.year_regex.match(release_date)
        if match:
            year, month, day = match.group(), '1', '1'
            return cls.validate_release_date(year, month, day)
        # other: "?", "????", "None", "Unknown"
        return None

    @classmethod
    def validate_release_date(cls, year, month, day):
        try:
            year = int(year)
            if month.isdigit():
                month = int(month)
            if month < 1:
                month = 1
            if day.isdigit():
                day = int(day)
            if day < 1:
                day = 1
            date = datetime.datetime(year, month, 1, 0, 0)
            day_offset = day - 1
            date = date + datetime.timedelta(days=day_offset)
        except ValueError:
            traceback.print_exc()
            print('BAD DATE:', year, month, day)
            date = None
        return date


Release._tags_to_fields_mapping = {
    'artists': ('artists', ArtistCredit.from_elements),
    'companies': ('companies', CompanyCredit.from_elements),
    'country': ('country', Bootstrap.element_to_string),
    'data_quality': ('data_quality', Bootstrap.element_to_string),
    'extraartists': ('extra_artists', ArtistCredit.from_elements),
    'formats': ('formats', Format.from_elements),
    'genres': ('genres', Bootstrap.element_to_strings),
    'identifiers': ('identifiers', Identifier.from_elements),
    'labels': ('labels', LabelCredit.from_elements),
    'master_id': ('master_id', Bootstrap.element_to_integer),
    'released': ('release_date', Bootstrap.element_to_datetime),
    'styles': ('styles', Bootstrap.element_to_strings),
    'title': ('title', Bootstrap.element_to_string),
    'tracklist': ('tracklist', Track.from_elements),
    }