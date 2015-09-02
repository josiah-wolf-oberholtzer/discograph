import gzip
import mongoengine
from discograph.models.Model import Model


class Master(Model, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    data_quality = mongoengine.StringField()
    discogs_id = mongoengine.IntField(unique=True, null=True, sparse=True)
    genres = mongoengine.ListField(mongoengine.StringField())
    main_release_id = mongoengine.IntField()
    release_date = mongoengine.DateTimeField()
    styles = mongoengine.ListField(mongoengine.StringField())
    title = mongoengine.StringField()

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
        from discograph.bootstrap import Bootstrap
        cls.drop_collection()
        masters_xml_path = Bootstrap.masters_xml_path
        with gzip.GzipFile(masters_xml_path, 'r') as file_pointer:
            masters_iterator = Bootstrap.iterparse(file_pointer, 'master')
            masters_iterator = Bootstrap.clean_elements(masters_iterator)
            for master_element in masters_iterator:
                master_document = cls.from_element(master_element)
                print(u'MASTER {}: {}'.format(
                    master_document.discogs_id,
                    master_document.title,
                    ))

    @classmethod
    def from_element(cls, element):
        from discograph import models
        artists = element.find('artists')
        if artists is not None and len(artists):
            artists = [models.ArtistCredit.from_element(_) for _ in artists]
        else:
            artists = None
        # data quality
        data_quality = element.find('data_quality').text
        # discogs id
        discogs_id = int(element.attrib.get('id'))
        # genres
        genres = element.find('genres')
        if genres is not None and len(genres):
            genres = [_.text for _ in genres]
        else:
            genres = None
        # main release
        main_release = element.find('main_release')
        if main_release is not None:
            main_release = int(main_release.text)
            main_release = models.Release.objects.get(discogs_id=main_release)
        # release_date
        release_date = element.find('year')
        if release_date is not None:
            release_date = models.Release.parse_release_date(release_date.text)
        # styles
        styles = element.find('styles')
        if styles is not None and len(styles):
            styles = [_.text for _ in styles]
        else:
            styles = None
        # title
        title = element.find('title').text
        # construct
        master_document = cls(
            artists=artists,
            data_quality=data_quality,
            discogs_id=discogs_id,
            genres=genres,
            main_release=main_release,
            release_date=release_date,
            styles=styles,
            title=title,
            )
        return master_document