from __future__ import print_function
import gzip
import mongoengine
import traceback
from abjad.tools import systemtools
from discograph.models.Model import Model


class Artist(Model, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    discogs_id = mongoengine.IntField(required=True, unique=True)
    name = mongoengine.StringField(required=True, unique=True)
    real_name = mongoengine.StringField(null=True)
    name_variations = mongoengine.ListField(mongoengine.StringField())
    aliases = mongoengine.ListField(mongoengine.StringField())
    members = mongoengine.ListField(mongoengine.ReferenceField('Artist'))
    # "groups" is inverse of "members", and therefore derived.
    groups = mongoengine.ListField(mongoengine.ReferenceField('Artist'))
    has_been_scraped = mongoengine.BooleanField(default=False)

    ### MONGOENGINE META ###

    meta = {
        'indexes': [
            'discogs_id',
            'name',
            ('$name', '$real_name', '$aliases', '$name_variations'),
            ],
        }

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        keyword_argument_names = sorted(self._fields)
        if 'id' in keyword_argument_names:
            keyword_argument_names.remove('id')
        if 'groups' in keyword_argument_names:
            keyword_argument_names.remove('groups')
        for keyword_argument_name in keyword_argument_names[:]:
            value = getattr(self, keyword_argument_name)
            if isinstance(value, list) and not value:
                keyword_argument_names.remove(keyword_argument_name)
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        from discograph.bootstrap import Bootstrap
        cls.drop_collection()
        artists_xml_path = Bootstrap.artists_xml_path
        with gzip.GzipFile(artists_xml_path, 'r') as file_pointer:
            artists_iterator = Bootstrap.iterparse(file_pointer, 'artist')
            artists_iterator = Bootstrap.clean_elements(artists_iterator)
            for artist_element in artists_iterator:
                artist_document = cls.from_element(artist_element)
                print(u'ARTIST {}: {}'.format(
                    artist_document.discogs_id,
                    artist_document.name,
                    ))

    def extract_relations(self):
        from discograph import models
        relations = []
        if not self.members:
            return relations
        for member in self.members:
            relation = models.ArtistArtistRelation(
                artist_one=member,
                artist_two=self,
                role='Member',
                )
            relations.append(relation)
        return relations

    @classmethod
    def from_id_and_name(cls, discogs_id, name):
        index = [('discogs_id', 1)]
        query_set = cls.objects(discogs_id=discogs_id)\
            .hint(index)\
            .only('discogs_id', 'has_been_scraped', 'name')\
            .no_dereference()
        if query_set.count():
            return query_set[0]
        document = cls(discogs_id=discogs_id, name=name)
        document.save()
        return document

    @classmethod
    def from_element(cls, element):
        discogs_id = int(element.find('id').text)
        name = element.find('name')
        if name is not None:
            name = name.text
        name = name or ''
        artist_document = cls.from_id_and_name(discogs_id, name)
        if artist_document.has_been_scraped:
            return artist_document
        real_name = element.find('name')
        if real_name is not None:
            real_name = real_name.text
        real_name = real_name or ''
        name_variations = element.find('namevariations')
        if name_variations is None or not len(name_variations):
            name_variations = []
        name_variations = [_.text for _ in name_variations if _.text]
        aliases = element.find('aliases')
        if aliases is None or not len(aliases):
            aliases = []
        aliases = [_.text for _ in aliases if _.text]
        members = element.find('members')
        member_documents = []
        if members is not None and len(members):
            for i in range(0, len(members), 2):
                member_id = int(members[i].text)
                member_name = members[i + 1].text
                member_document = cls.from_id_and_name(member_id, member_name)
                member_document.groups.append(artist_document)
                member_document.save()
                member_documents.append(member_document)
        artist_document.real_name = real_name
        artist_document.name_variations = name_variations
        artist_document.aliases = aliases
        artist_document.has_been_scraped = True
        artist_document.members = member_documents
        try:
            artist_document.save()
        except mongoengine.errors.ValidationError as exception:
            traceback.print_exc()
            print('ERROR:', discogs_id, name)
            print('    real name:      ', real_name)
            print('    name variations:', name_variations)
            print('    aliases:        ', aliases)
            print('    members:        ', member_documents)
            raise exception
        return artist_document