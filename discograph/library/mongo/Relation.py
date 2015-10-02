# -*- encoding: utf-8 -*-
import collections
import itertools
import mongoengine
import os
import pprint
import pymongo.errors
import pymongo.operations
import random
from abjad.tools import datastructuretools
from abjad.tools import systemtools
from discograph.library.mongo.MongoModel import MongoModel
from discograph.library.mongo.Artist import Artist
from discograph.library.mongo.Label import Label


class Relation(MongoModel, mongoengine.Document):

    ### CLASS VARIABLES ###

    Reference = collections.namedtuple(
        'Reference',
        ['class_', 'discogs_id', 'name'],
        )

    class EntityType(datastructuretools.Enumeration):
        ARTIST = 1
        LABEL = 2

    _model_to_entity_type = {
        Artist: EntityType.ARTIST,
        Label: EntityType.LABEL,
        }

    ### MONGOENGINE FIELDS ###

    hash_id = mongoengine.IntField(primary_key=True)
    category = mongoengine.IntField(null=True)
    country = mongoengine.StringField(null=True)
    entity_one_id = mongoengine.IntField()
    entity_one_type = mongoengine.IntField()
    entity_two_id = mongoengine.IntField()
    entity_two_type = mongoengine.IntField()
    genres = mongoengine.ListField(mongoengine.StringField(), null=True)
    release_id = mongoengine.IntField(null=True)
    role_name = mongoengine.StringField()
    styles = mongoengine.ListField(mongoengine.StringField(), null=True)
    subcategory = mongoengine.IntField(null=True)
    year = mongoengine.IntField(null=True)

    ### MONOGENGINE META ###

    meta = {
        'indexes': [

            ('entity_one_type', 'entity_one_id', 'role_name'),
            ('entity_two_type', 'entity_two_id', 'role_name'),

            ('role_name', 'entity_one_type', 'entity_one_id'),
            ('role_name', 'entity_two_type', 'entity_two_id'),

            ('role_name', 'entity_one_id'),
            ('role_name', 'entity_two_id'),

            ('entity_one_id', 'entity_one_type', 'role_name'),
            ('entity_two_id', 'entity_two_type', 'role_name'),

            ]
        }

    ### PRIVATE METHODS ###

    @classmethod
    def _bulk_insert(cls, relations):
        if not relations:
            return
        bulk = cls._get_collection().initialize_unordered_bulk_op()
        for relation in relations:
            bulk.insert(relation)
        try:
            bulk.execute()
        except pymongo.errors.BulkWriteError as bwe:
            pprint.pprint(bwe.details)

    @classmethod
    def _get_categories(cls, role_name):
        from discograph import library
        categories = library.CreditRole.all_credit_roles.get(
            role_name, None)
        if not categories:
            return None, None
        if len(categories) == 1:
            return categories[0], None
        return categories

    @classmethod
    def _get_hash_id(cls, document):
        category = document['category']
        country = document['country']
        genres = document['genres']
        if genres is not None:
            genres = tuple(genres)
        genres = genres or None
        entity_one_id = document['entity_one_id']
        entity_one_type = document['entity_one_type']
        entity_two_id = document['entity_two_id']
        entity_two_type = document['entity_two_type']
        #is_trivial = document['is_trivial']
        release_id = document['release_id']
        role_name = document['role_name']
        styles = document['styles']
        if styles is not None:
            styles = tuple(styles)
        styles = styles or None
        subcategory = document['subcategory']
        year = document['year']
        hash_values = (
            category,
            country,
            genres,
            entity_one_id,
            entity_one_type,
            entity_two_id,
            entity_two_type,
            #is_trivial,
            release_id,
            role_name,
            styles,
            subcategory,
            year,
            )
        return hash(hash_values)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from discograph import library
        keyword_argument_names = sorted(self._fields)
        if 'id' in keyword_argument_names:
            keyword_argument_names.remove('id')
        if 'hash_id' in keyword_argument_names:
            keyword_argument_names.remove('hash_id')
        keyword_argument_callables = dict(
            category=library.CreditRole.Category,
            entity_one_type=self.EntityType,
            entity_two_type=self.EntityType,
            subcategory=library.CreditRole.Subcategory,
            )
        for keyword_argument_name in keyword_argument_names[:]:
            value = getattr(self, keyword_argument_name)
            if isinstance(value, list) and not value:
                keyword_argument_names.remove(keyword_argument_name)
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            keyword_argument_callables=keyword_argument_callables,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def model_to_tuple(cls, reference):
        from discograph import library
        if isinstance(reference, cls.Reference):
            return reference
        class_ = library.Artist
        prototype = (
            library.Label,
            library.LabelCredit,
            library.LabelReference,
            )
        if isinstance(reference, prototype):
            class_ = library.Label
        result = cls.Reference(
            class_=class_,
            discogs_id=reference.discogs_id,
            name=reference.name,
            )
        #print(reference, result)
        return result

    @classmethod
    def bootstrap(cls):
        #cls.drop_collection()
        #cls.bootstrap_pass_one()
        #cls.bootstrap_pass_two()
        cls.bootstrap_pass_three()

    @classmethod
    def bootstrap_pass_one(cls):
        from discograph import library
        query = library.Artist.objects.no_cache().timeout(False)
        for i, artist in enumerate(query):
            print('(idx:{}) (id:{}) {}'.format(
                i,
                artist.discogs_id,
                artist.name,
                ))
            relations = cls.from_artist(artist)
            cls._bulk_insert(relations)

    @classmethod
    def bootstrap_pass_two(cls):
        from discograph import library
        query = library.Label.objects.no_cache().timeout(False)
        for i, label in enumerate(query):
            print('(idx:{}) (id:{}) {}'.format(
                i,
                label.discogs_id,
                label.name,
                ))
            relations = cls.from_label(label)
            cls._bulk_insert(relations)

    @classmethod
    def bootstrap_pass_three(cls):
        from discograph import library
        query = library.Release.objects.no_cache().timeout(False)
        for i, release in enumerate(query):
            print('(idx:{}) (id:{}) {}'.format(
                i,
                release.discogs_id,
                release.title,
                ))
            relations = cls.from_release(release)
            cls._bulk_insert(relations)

    @classmethod
    def count_roles(cls):
        query = cls.objects.aggregate(
            {'$match': {}},
            {'$group': {'_id': '$role_name', 'total': {'$sum': 1}}},
            )
        result = {}
        for item in query:
            role = item['_id']
            total = item['total']
            result[role] = total
        return result

    @classmethod
    def dump_to_csv(cls, file_path=None):
        import discograph
        if file_path is None:
            file_path = os.path.join(
                discograph.__path__[0],
                'data',
                '{}.csv'.format(cls.__name__.lower()),
                )
        count = cls.objects.count()
        query = cls._get_collection().find(no_cursor_timeout=True)
        file_pointer = open(file_path, 'w')
        progress_indicator = systemtools.ProgressIndicator(
            message='Processing', total=count)
        with file_pointer, progress_indicator:
            #line = ','.join([
            #    'id',
            #    'entity_one_id',
            #    'entity_one_type',
            #    'entity_two_id',
            #    'entity_two_type',
            #    'release_id',
            #    'role_name',
            #    'year',
            #    ]) + '\n'
            #file_pointer.write(line)
            iterator = iter(query)
            for i in range(count):
                try:
                    document = next(iterator)
                except Exception:
                    print('ERROR:', i)
                    print()
                    continue
                data = [
                    i,
                    document['entity_one_id'],
                    document['entity_one_type'],
                    document['entity_two_id'],
                    document['entity_two_type'],
                    ]
                data.append(document.get('release_id', None) or '')
                data.append('"{}"'.format(document['role_name']))
                data.append(document.get('year', None) or '')
                line = ';'.join(str(_) for _ in data) + '\n'
                file_pointer.write(line)
                progress_indicator.advance()

    @staticmethod
    def dump_to_sqlite():
        import discograph
        discograph.SqliteRelation.drop_table(fail_silently=True)
        discograph.SqliteRelation.create_table()
        count = discograph.Relation.objects.count()
        query = discograph.Relation._get_collection().find()
        rows = []
        for i, mongo_document in enumerate(query, 1):
            rows.append(dict(
                id=i,
                entity_one_id=mongo_document.get('entity_one_id'),
                entity_one_type=mongo_document.get('entity_one_type'),
                entity_two_id=mongo_document.get('entity_two_id'),
                entity_two_type=mongo_document.get('entity_two_type'),
                year=mongo_document.get('year'),
                release_id=mongo_document.get('release_id'),
                role_name=mongo_document.get('role_name'),
                random=random.random(),
                ))
            if mongo_document.get('role_name') not in ('Alias', 'Member Of'):
                break
            if len(rows) == 100:
                discograph.SqliteRelation.insert_many(rows).execute()
                rows = []
                print('Processing... {} of {} [{:.3f}%]'.format(
                    i, count, (float(i) / count) * 100))
        if rows:
            discograph.SqliteRelation.insert_many(rows).execute()
            print('Processing... {} of {} [{:.3f}%]'.format(
                i, count, (float(i) / count) * 100))

    @classmethod
    def from_artist(cls, artist):
        triples = set()
        role = 'Alias'
        for alias in artist.aliases:
            if not alias.discogs_id:
                continue
            artist_one, artist_two = sorted(
                [artist, alias],
                key=lambda x: x.discogs_id,
                )
            entity_one = cls.model_to_tuple(artist_one)
            entity_two = cls.model_to_tuple(artist_two)
            triples.add((entity_one, role, entity_two))
        role = 'Member Of'
        for member in artist.members:
            entity_one = cls.model_to_tuple(member)
            entity_two = cls.model_to_tuple(artist)
            triples.add((entity_one, role, entity_two))
        key_function = lambda x: (x[0].discogs_id, x[1], x[2].discogs_id)
        triples = (_ for _ in triples
            if all((_[0].discogs_id, _[1], _[2].discogs_id))
            )
        triples = sorted(triples, key=key_function)
        relations = cls.from_triples(triples)
        return relations

    @classmethod
    def from_label(cls, label):
        if not label.discogs_id:
            return []
        triples = set()
        role = 'Sublabel Of'
        for sublabel in label.sublabels:
            if not sublabel.discogs_id:
                continue
            entity_one = cls.model_to_tuple(sublabel)
            entity_two = cls.model_to_tuple(label)
            triples.add((entity_one, role, entity_two))
        key_function = lambda x: (x[0].discogs_id, x[1], x[2].discogs_id)
        triples = (_ for _ in triples
            if all((_[0].discogs_id, _[1], _[2].discogs_id))
            )
        triples = sorted(triples, key=key_function)
        relations = cls.from_triples(triples)
        return relations

    @classmethod
    def from_triples(cls, triples, release=None):
        from discograph import library
        #for triple in triples:
        #    print(triple)
        relations = []
        (
            country,
            genres,
            release_id,
            styles,
            year,
            ) = None, [], None, [], None
        if release is not None:
            release_id = release.discogs_id
            if release.release_date is not None:
                year = release.release_date.year
            country = release.country or None
            genres = [] or release.genres or []
            styles = [] or release.styles or []
        for entity_one, role_name, entity_two in triples:
            entity_one_type = cls.EntityType.ARTIST
            if issubclass(entity_one.class_, (library.Label, library.LabelReference)):
                entity_one_type = cls.EntityType.LABEL
            entity_two_type = cls.EntityType.ARTIST
            if issubclass(entity_two.class_, (library.Label, library.LabelReference)):
                entity_two_type = cls.EntityType.LABEL
            category, subcategory = cls._get_categories(role_name)
            #is_trivial = None
            #if (
            #    entity_one_type == entity_two_type == cls.EntityType.ARTIST and
            #    role_name not in ('Member Of', 'Alias')
            #    ):
            #    if entity_one.discogs_id == entity_two.discogs_id:
            #        is_trivial = True
            #    if entity_one in entity_two.members:
            #        is_trivial = True
            #    if entity_one.name in entity_two.aliases:
            #        is_trivial = True
            #    if entity_two.name in entity_one.aliases:
            #        is_trivial = True
            #relation = dict(
            relation = cls(
                category=category,
                country=country,
                entity_one_id=entity_one.discogs_id,
                entity_one_type=entity_one_type,
                entity_two_id=entity_two.discogs_id,
                entity_two_type=entity_two_type,
                genres=genres,
                release_id=release_id,
                role_name=role_name,
                styles=styles,
                subcategory=subcategory,
                year=year,
                )
            #relation.hash_id = Relation._get_hash_id(relation)
            hash_id = Relation._get_hash_id(relation)
            relation['hash_id'] = hash_id
            relations.append(relation)
        return relations

    @classmethod
    def from_release(cls, release):
        from discograph import library

        triples = set()
        is_compilation = False
        artists = set(cls.model_to_tuple(_) for _ in release.artists)
        labels = set(cls.model_to_tuple(_) for _ in release.labels)
        if len(artists) == 1 and list(artists)[0].name == 'Various':
            is_compilation = True
            artists.clear()
            for track in release.tracklist:
                artists.update(cls.model_to_tuple(_) for _ in track.artists)
        for format_ in release.formats:
            for description in format_.descriptions:
                if description == 'Compilation':
                    is_compilation = True
                    break

        # Handle Artist-Label release relations.
        iterator = itertools.product(artists, labels)
        if is_compilation:
            role = 'Compiled On'
        else:
            role = 'Released On'
        for artist, label in iterator:
            entity_one = cls.model_to_tuple(artist)
            entity_two = cls.model_to_tuple(label)
            triples.add((entity_one, role, entity_two))

        # TODO: Filter out "Hosted By", "Presenter", "DJ Mix", "Compiled By"
        aggregate_roles = {}
        aggregate_role_names = (
            'Compiled By',
            'Curated By',
            'DJ Mix',
            'Hosted By',
            'Presenter',
            )

        # Handle release-global extra artists.
        if is_compilation:
            iterator = itertools.product(labels, release.extra_artists)
        else:
            iterator = itertools.product(artists, release.extra_artists)
        for entity_two, credit in iterator:
            entity_two = cls.model_to_tuple(entity_two)
            for role in credit.roles:
                role_name = role.name
                if role_name not in library.CreditRole.all_credit_roles:
                    continue
                elif role_name in aggregate_role_names:
                    if role_name not in aggregate_roles:
                        aggregate_roles[role_name] = []
                    aggregate_roles[role_name].append(credit)
                    continue
                entity_one = cls.model_to_tuple(credit)
                triples.add((entity_one, role_name, entity_two))

        # Handle extra artists on individual tracks.
        all_track_artists = set()
        for track in release.tracklist:
            track_artists = set(cls.model_to_tuple(_) for _ in track.artists)
            all_track_artists.update(track_artists)
            track_artists = track_artists or artists or labels
            iterator = itertools.product(track_artists, track.extra_artists)
            for entity_two, credit in iterator:
                entity_two = cls.model_to_tuple(entity_two)
                for role in credit.roles:
                    role_name = role.name
                    if role_name not in library.CreditRole.all_credit_roles:
                        continue
                    entity_one = cls.model_to_tuple(credit)
                    triples.add((entity_one, role_name, entity_two))

        # Handle aggregate artists (DJ, Compiler, Curator, Presenter, etc.)
        for role_name, aggregate_artists in aggregate_roles.items():
            iterator = itertools.product(all_track_artists, aggregate_artists)
            for track_artist, aggregate_artist in iterator:
                entity_one = cls.model_to_tuple(aggregate_artist)
                entity_two = cls.model_to_tuple(track_artist)
                triples.add((entity_one, role_name, entity_two))

        key_function = lambda x: (
            getattr(x[0], 'discogs_id', 0) or 0,
            getattr(x[2], 'discogs_id', 0) or 0,
            x[1],
            x[0].name,
            x[2].name,
            )
        triples = (_ for _ in triples
            if all((_[0].discogs_id, _[1], _[2].discogs_id))
            )
        triples = sorted(triples, key=key_function)
        relations = cls.from_triples(triples, release=release)
        return relations