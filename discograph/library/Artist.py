# -*- encoding: utf-8 -*-
from __future__ import print_function
import gzip
import mongoengine
import os
import random
import traceback
from abjad.tools import systemtools
from discograph.library.Bootstrapper import Bootstrapper
from discograph.library.ArtistReference import ArtistReference
from discograph.library.mongo.MongoModel import MongoModel


class Artist(MongoModel, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    discogs_id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField(required=True, unique=True)
    real_name = mongoengine.StringField()
    name_variations = mongoengine.ListField(mongoengine.StringField())
    aliases = mongoengine.EmbeddedDocumentListField('ArtistReference')
    members = mongoengine.EmbeddedDocumentListField('ArtistReference')
    groups = mongoengine.EmbeddedDocumentListField('ArtistReference')
    #has_been_scraped = mongoengine.BooleanField(default=False)

    ### MONGOENGINE META ###

    meta = {
        'indexes': [
            '#name',
            '$name',
            'discogs_id',
            'name',
            ],
        }

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        keyword_argument_names = sorted(self._fields)
        if 'id' in keyword_argument_names:
            keyword_argument_names.remove('id')
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
        cls.drop_collection()
        cls.bootstrap_pass_one()
        cls.bootstrap_pass_two()

    @classmethod
    def bootstrap_pass_one(cls):
        # Pass one.
        artists_xml_path = Bootstrapper.artists_xml_path
        with gzip.GzipFile(artists_xml_path, 'r') as file_pointer:
            iterator = Bootstrapper.iterparse(file_pointer, 'artist')
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
                        document.name,
                        )
                    print(message)
                except mongoengine.errors.ValidationError:
                    traceback.print_exc()

    @classmethod
    def bootstrap_pass_two(cls):
        # Pass two.
        cls.ensure_indexes()
        query = cls.objects().no_cache().timeout(False)
        query = query.only(
            'aliases',
            'discogs_id',
            'groups',
            'name',
            )
        for i, document in enumerate(query):
            with systemtools.Timer(verbose=False) as timer:
                changed = document.resolve_references()
            if not changed:
                message = u'{} [SKIPPED] (Pass 2) (idx:{}) (id:{}) [{:.8f}]: {}'.format(
                    cls.__name__.upper(),
                    i,
                    document.discogs_id,
                    timer.elapsed_time,
                    document.name,
                    )
                print(message)
                continue
            document.save()
            assert not document.resolve_references()
            message = u'{} (Pass 2) (idx:{}) (id:{}) [{:.8f}]: {}'.format(
                cls.__name__.upper(),
                i,
                document.discogs_id,
                timer.elapsed_time,
                document.name,
                )
            print(message)

    @classmethod
    def dump_to_csv(cls, file_path=None):
        import discograph
        if file_path is None:
            file_path = os.path.join(
                discograph.__path__[0],
                'data',
                '{}.csv'.format(cls.__name__.lower()),
                )
        query = cls.objects().no_cache().timeout(False)
        count = query.count()
        file_pointer = open(file_path, 'w')
        progress_indicator = systemtools.ProgressIndicator(
            message='Processing', total=count)
        with file_pointer, progress_indicator:
            line = 'id;name\n'
            file_pointer.write(line)
            for document in query:
                discogs_id = document.discogs_id
                name = document.name
                if discogs_id and name:
                    name = name.replace('"', r'\"')
                    line = '{};"{}"\n'.format(discogs_id, name)
                    file_pointer.write(line)
                progress_indicator.advance()

    @staticmethod
    def dump_to_sqlite():
        import discograph
        discograph.SqliteFTSArtist.drop_table(True)
        discograph.SqliteArtist.drop_table(True)
        discograph.SqliteArtist.create_table()
        discograph.SqliteFTSArtist.create_table(
            content=discograph.SqliteArtist,
            tokenize='porter',
            )
        query = discograph.Artist.objects().no_cache().timeout(False)
        query = query.only('discogs_id', 'name')
        count = query.count()
        rows = []
        for i, mongo_document in enumerate(query, 1):
            if mongo_document.discogs_id and mongo_document.name:
                rows.append(dict(
                    id=mongo_document.discogs_id,
                    name=mongo_document.name,
                    random=random.random(),
                    ))
            if len(rows) == 100:
                discograph.SqliteArtist.insert_many(rows).execute()
                rows = []
                print('Processing... {} of {} [{:.3f}%]'.format(
                    i, count, (float(i) / count) * 100))
        if rows:
            discograph.SqliteArtist.insert_many(rows).execute()
            print('Processing... {} of {} [{:.3f}%]'.format(
                i, count, (float(i) / count) * 100))
        discograph.SqliteFTSArtist.rebuild()
        discograph.SqliteFTSArtist.optimize()

    @classmethod
    def from_element(cls, element):
        data = cls.tags_to_fields(element)
        document = cls(**data)
        return document

    def get_relations(
        self,
        include_aliases=False,
        exclude_trivial=False,
        ):
        from discograph import library
        ids = [self.discogs_id]
        if include_aliases:
            for alias in self.aliases:
                query = library.Artist.objects(name=alias)
                query = query.hint([('name', 'hashed')])
                if not query.count():
                    continue
                alias = query.first()
                ids.append(alias.discogs_id)
        composite = (
            mongoengine.Q(
                entity_one_id__in=ids,
                entity_one_type=library.Relation.EntityType.ARTIST,
                ) |
            mongoengine.Q(
                entity_two_id__in=ids,
                entity_two_type=library.Relation.EntityType.ARTIST,
                )
            )
        query = library.Relation.objects(composite)
        if exclude_trivial:
            query = query(is_trivial__ne=True)
        return query

    def get_relation_counts(
        self,
        include_aliases=False,
        exclude_trivial=False,
        ):
        query = self.get_relations(
            include_aliases=include_aliases,
            exclude_trivial=exclude_trivial,
            )
        query = query.item_frequencies('year')
        results = sorted(
            (year, count)
            for year, count in query.items()
            if year
            )
        return results

    def get_relation_agggregate(
        self,
        include_aliases=False,
        exclude_trivial=False,
        ):
        from discograph import library
        ids = [self.discogs_id]
        if include_aliases:
            for alias in self.aliases:
                query = library.Artist.objects(name=alias)
                query = query.hint([('name', 'hashed')])
                if not query.count():
                    continue
                alias = query.first()
                ids.append(alias.discogs_id)
        query = library.Relation.objects.aggregate(
            {'$match': {
                'entity_one_id': {'$in': ids},
                'entity_one_type': 1,
                'year': {'$exists': 1},
                }},
            {'$group': {
                '_id': {
                    'year': '$year',
                    'role_name': '$role_name',
                    },
                'total': {'$sum': 1}
                }},
            {'$group': {
                '_id': '$_id.year',
                'totals': {
                    '$push': {
                        'role_name': '$_id.role_name',
                        'total': '$total',
                        },
                    },
                }},
            {'$project': {'_id': 0, 'year': '$_id', 'totals': '$totals'}},
            {'$sort': {'year': 1}}
            )
        return query

    def resolve_references(self):
        changed = False
        for reference in self.aliases:
            query = type(self).objects(name=reference.name)
            query = query.only('discogs_id', 'name')
            found = list(query)
            if len(found) and found[0].discogs_id != reference.discogs_id:
                reference.discogs_id = found[0].discogs_id
                changed = True
            elif not len(found) and reference.discogs_id:
                reference.discogs_id = None
                changed = True
        for reference in self.members:
            query = type(self).objects(name=reference.name)
            query = query.only('discogs_id', 'name')
            found = list(query)
            if len(found) and found[0].discogs_id != reference.discogs_id:
                reference.discogs_id = found[0].discogs_id
                changed = True
            elif not len(found) and reference.discogs_id:
                reference.discogs_id = None
                changed = True
        for reference in self.groups:
            query = type(self).objects(name=reference.name)
            query = query.only('discogs_id', 'name')
            found = list(query)
            if len(found) and found[0].discogs_id != reference.discogs_id:
                reference.discogs_id = found[0].discogs_id
                changed = True
            elif not len(found) and reference.discogs_id:
                reference.discogs_id = None
                changed = True
        return changed

    @classmethod
    def search_text(cls, search_string='', limit=10):
        query = cls.objects.search_text(search_string).order_by('$text_score')
        query = query.limit(limit).only('discogs_id', 'name').as_pymongo()
        result = list(query)
        return result


Artist._tags_to_fields_mapping = {
    'id': ('discogs_id', Bootstrapper.element_to_integer),
    'name': ('name', Bootstrapper.element_to_string),
    'realname': ('real_name', Bootstrapper.element_to_string),
    'namevariations': ('name_variations', Bootstrapper.element_to_strings),
    'aliases': ('aliases', ArtistReference.from_names),
    'groups': ('groups', ArtistReference.from_names),
    'members': ('members', ArtistReference.from_members),
    }