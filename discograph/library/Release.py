from __future__ import print_function
import datetime
import gzip
import mongoengine
import re
import traceback
from abjad.tools import systemtools
from discograph.library.Bootstrapper import Bootstrapper
from discograph.library.ArtistCredit import ArtistCredit
from discograph.library.CompanyCredit import CompanyCredit
from discograph.library.Format import Format
from discograph.library.Identifier import Identifier
from discograph.library.LabelCredit import LabelCredit
from discograph.library.Model import Model
from discograph.library.Track import Track


class Release(Model, mongoengine.Document):

    ### CLASS VARIABLES ###

    date_regex = re.compile('^(\d{4})-(\d{2})-(\d{2})$')
    date_no_dashes_regex = re.compile('^(\d{4})(\d{2})(\d{2})$')
    year_regex = re.compile('^\d\d\d\d$')

    ### MONGOENGINE FIELDS ###

    discogs_id = mongoengine.IntField(primary_key=True)
    artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    companies = mongoengine.EmbeddedDocumentListField('CompanyCredit')
    country = mongoengine.StringField()
    #data_quality = mongoengine.StringField()
    extra_artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    formats = mongoengine.EmbeddedDocumentListField('Format')
    genres = mongoengine.ListField(mongoengine.StringField())
    identifiers = mongoengine.EmbeddedDocumentListField('Identifier')
    labels = mongoengine.EmbeddedDocumentListField('LabelCredit')
    master_id = mongoengine.IntField()
    release_date = mongoengine.DateTimeField()
    #status = mongoengine.StringField()
    styles = mongoengine.ListField(mongoengine.StringField())
    title = mongoengine.StringField()
    tracklist = mongoengine.EmbeddedDocumentListField('Track')

    ### MONGOENGINE META ###

    meta = {
        'indexes': [
            '#title',
            '$title',
            'discogs_id',
            'title',
            ],
        }

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        #cls.drop_collection()
        #cls.bootstrap_pass_one()
        cls.bootstrap_pass_two()

    @classmethod
    def bootstrap_pass_one(cls):
        # Pass one.
        releases_xml_path = Bootstrapper.releases_xml_path
        with gzip.GzipFile(releases_xml_path, 'r') as file_pointer:
            iterator = Bootstrapper.iterparse(file_pointer, 'release')
            iterator = Bootstrapper.clean_elements(iterator)
            for i, element in enumerate(iterator):
                try:
                    with systemtools.Timer(verbose=False) as timer:
                        document = cls.from_element(element)
                        cls.objects.insert(document, load_bulk=False)
                        #document.save()
                        #document.save(force_insert=True)
                    message = u'{} (Pass 1) {} [{}]: {}'.format(
                        cls.__name__.upper(),
                        document.discogs_id,
                        timer.elapsed_time,
                        document.title,
                        )
                    print(message)
                except mongoengine.errors.ValidationError:
                    traceback.print_exc()

    @classmethod
    def bootstrap_pass_two(cls):
        from discograph import library
        # Pass two.
        cls.ensure_indexes()
        library.Artist.ensure_indexes()
        library.Label.ensure_indexes()
        label_corpus = library.Label.get_label_corpus()
        query = cls.objects().no_cache()
        query = query.only(
            'companies',
            'discogs_id',
            'labels',
            'title',
            )
        for i, document in enumerate(query):
            with systemtools.Timer(verbose=False) as timer:
                changed = document.resolve_references_no_query(
                    label_corpus=label_corpus)
                if changed:
                    document.save()
            message = u'{} (Pass 2) (idx:{}) (id:{}) [{:.8f}]: {}'.format(
                cls.__name__.upper(),
                i,
                document.discogs_id,
                timer.elapsed_time,
                document.title,
                )
            print(message)

    def resolve_references(self, spuriously=False):
        from discograph import library
        changed = False
        spurious_discogs_id = 0
        spurious_references = {}
        for company_credit in self.companies:
            query = library.Label.objects(name=company_credit.name)
            query = query.no_cache()
            query = query.hint([('name', 1)])
            query = query.only('discogs_id', 'name')
            found = list(query)
            if not len(found):
                if spuriously:
                    if company_credit.name not in spurious_references:
                        spurious_discogs_id -= 1
                        spurious_references[company_credit.name] = spurious_discogs_id
                    company_credit.discogs_id = spurious_references[company_credit.name]
                continue
            company_credit.discogs_id = found[0].discogs_id
            changed = True
        for label_credit in self.labels:
            query = library.Label.objects(name=label_credit.name)
            query = query.no_cache()
            query = query.hint([('name', 1)])
            query = query.only('discogs_id', 'name')
            found = list(query)
            if not len(found):
                if spuriously:
                    if label_credit.name not in spurious_references:
                        spurious_discogs_id -= 1
                        spurious_references[label_credit.name] = spurious_discogs_id
                    label_credit.discogs_id = spurious_references[label_credit.name]
                continue
            label_credit.discogs_id = found[0].discogs_id
            changed = True
        return changed

    def resolve_references_no_query(self, label_corpus=None, spuriously=False):
        changed = False
        spurious_discogs_id = 0
        spurious_references = {}
        credits = []
        credits.extend(self.companies)
        credits.extend(self.labels)
        for credit in credits:
            if credit.name not in label_corpus:
                if spuriously:
                    if credit.name not in spurious_references:
                        spurious_discogs_id -= 1
                        spurious_references[credit.name] = spurious_discogs_id
                    credit.discogs_id = spurious_references[credit.name]
                    changed = True
                continue
            credit.discogs_id = label_corpus[credit.name]
            changed = True
        return changed

    @classmethod
    def from_element(cls, element):
        discogs_id = int(element.attrib.get('id'))
        data = cls.tags_to_fields(element)
        data.update(discogs_id=discogs_id)
        document = cls(**data)
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
    'country': ('country', Bootstrapper.element_to_string),
    #'data_quality': ('data_quality', Bootstrapper.element_to_string),
    'extraartists': ('extra_artists', ArtistCredit.from_elements),
    'formats': ('formats', Format.from_elements),
    'genres': ('genres', Bootstrapper.element_to_strings),
    'identifiers': ('identifiers', Identifier.from_elements),
    'labels': ('labels', LabelCredit.from_elements),
    'master_id': ('master_id', Bootstrapper.element_to_integer),
    'released': ('release_date', Bootstrapper.element_to_datetime),
    'styles': ('styles', Bootstrapper.element_to_strings),
    'title': ('title', Bootstrapper.element_to_string),
    'tracklist': ('tracklist', Track.from_elements),
    }