# -*- encoding: utf-8 -*-
import itertools
import peewee
import random
import multiprocessing
import re
import traceback
from abjad.tools import datastructuretools
from discograph.library.PostgresModel import PostgresModel
from playhouse import postgres_ext


class PostgresRelation(PostgresModel):

    ### CLASS VARIABLES ###

    class EntityType(datastructuretools.Enumeration):
        ARTIST = 1
        LABEL = 2

    class BootstrapWorker(multiprocessing.Process):

        corpus = {}

        def __init__(self, start, stop):
            multiprocessing.Process.__init__(self)
            self.indices = (start, stop)

        def run(self):
            proc_name = self.name
            start, stop = self.indices
            for release_id in range(start, stop + 1):
                try:
                    PostgresRelation.bootstrap_pass_three_inner(
                        release_id,
                        self.corpus,
                        annotation=proc_name,
                        )
                except:
                    traceback.print_exc()

    aggregate_roles = (
        'Compiled By',
        'Curated By',
        'DJ Mix',
        'Hosted By',
        'Presenter',
        )

    word_pattern = re.compile('\s+')

    ### PEEWEE FIELDS ###

    entity_one_type = peewee.IntegerField()
    entity_one_id = peewee.IntegerField()
    entity_two_type = peewee.IntegerField()
    entity_two_id = peewee.IntegerField()
    role = peewee.CharField()
    releases = postgres_ext.BinaryJSONField(null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'relations'
        primary_key = peewee.CompositeKey(
            'entity_one_type',
            'entity_one_id',
            'entity_two_type',
            'entity_two_id',
            'role',
            )
        indexes = (
            ((
                'entity_one_type', 'entity_one_id',
                'entity_two_type', 'entity_two_id',
                'role'), True),
            ((
                'entity_two_type', 'entity_two_id',
                'entity_one_type', 'entity_one_id',
                'role'), True),
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _as_artist_credits(cls, companies):
        artists = []
        for company in companies:
            artist = {
                'name': company['name'],
                'id': company['id'],
                'roles': [{'name': company['entity_type_name']}],
                }
            artists.append(artist)
        return artists

    ### PUBLIC METHODS ###

    def as_json(self):
        data = {
            'key': self.link_key,
            'role': self.role,
            'source': self.json_entity_one_key,
            'target': self.json_entity_two_key,
            }
        if hasattr(self, 'distance'):
            data['distance'] = self.distance
        if hasattr(self, 'pages'):
            data['pages'] = tuple(sorted(self.pages))
        return data

    @classmethod
    def bootstrap(cls):
        cls.drop_table(True)
        cls.create_table()
        cls.bootstrap_pass_three()

    @classmethod
    def bootstrap_pass_three(cls):
        import discograph
        release_class = discograph.PostgresRelease
        maximum_id = release_class.select(
            peewee.fn.Max(release_class.id)).scalar()
        step = maximum_id // (multiprocessing.cpu_count() * 2)
        workers = []
        for start in range(0, maximum_id, step):
            stop = start + step
            worker = cls.BootstrapWorker(start, stop)
            workers.append(worker)
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()
        for worker in workers:
            worker.terminate()

    @classmethod
    def bootstrap_pass_three_inner(cls, release_id, corpus, annotation=''):
        import discograph
        database = cls._meta.database
        with database.execution_context(with_transaction=False):
            release_cls = discograph.PostgresRelease
            query = release_cls.select().where(release_cls.id == release_id)
            if not query.count():
                return
            document = query.get()
            relations = cls.from_release(document)
            print('[{}] (id:{})           [{}] {}'.format(
                annotation,
                document.id,
                len(relations),
                document.title,
                ))
            for relation in relations:
                instance, created = cls.create_or_get(
                    entity_one_type=relation['entity_one_type'],
                    entity_one_id=relation['entity_one_id'],
                    entity_two_type=relation['entity_two_type'],
                    entity_two_id=relation['entity_two_id'],
                    role=relation['role'],
                    )
                if created:
                    instance.releases = {}
                if 'release_id' in relation:
                    release_id = relation['release_id']
                    year = relation.get('year')
                    instance.releases[release_id] = year
                instance.save()

    @classmethod
    def from_release(cls, release):
        import discograph
        triples = set()
        artists, labels, is_compilation = cls.get_release_setup(release)
        triples.update(cls.get_artist_label_relations(
            artists,
            labels,
            is_compilation,
            ))
        aggregate_roles = {}

        if is_compilation:
            iterator = itertools.product(labels, release.extra_artists)
        else:
            iterator = itertools.product(artists, release.extra_artists)
        for entity_two, credit in iterator:
            for role in credit['roles']:
                role = role['name']
                if role not in discograph.CreditRole.all_credit_roles:
                    continue
                elif role in cls.aggregate_roles:
                    if role not in aggregate_roles:
                        aggregate_roles[role] = []
                    aggregate_credit = (cls.EntityType.ARTIST, credit['id'])
                    aggregate_roles[role].append(aggregate_credit)
                    continue
                entity_one = (cls.EntityType.ARTIST, credit['id'])
                triples.add((entity_one, role, entity_two))

        if is_compilation:
            iterator = itertools.product(labels, release.companies)
        else:
            iterator = itertools.product(artists, release.companies)
        for entity_one, company in iterator:
                role = company['entity_type_name']
                if role not in discograph.CreditRole.all_credit_roles:
                    continue
                entity_two = (cls.EntityType.LABEL, company['id'])
                triples.add((entity_one, role, entity_two))

        all_track_artists = set()
        for track in release.tracklist:
            track_artists = set(
                (cls.EntityType.ARTIST, _['id'])
                for _ in track.get('artists', ())
                )
            all_track_artists.update(track_artists)
            if not track.get('extra_artists'):
                continue
            track_artists = track_artists or artists or labels
            iterator = itertools.product(track_artists, track['extra_artists'])
            for entity_two, credit in iterator:
                for role in credit.get('roles', ()):
                    role = role['name']
                    if role not in discograph.CreditRole.all_credit_roles:
                        continue
                    entity_one = (cls.EntityType.ARTIST, credit['id'])
                    triples.add((entity_one, role, entity_two))
        for role, aggregate_artists in aggregate_roles.items():
            iterator = itertools.product(all_track_artists, aggregate_artists)
            for track_artist, aggregate_artist in iterator:
                entity_one = aggregate_artist
                entity_two = track_artist
                triples.add((entity_one, role, entity_two))
        triples = sorted(triples)
        relations = cls.from_triples(triples, release=release)
        return relations

    @classmethod
    def get_artist_label_relations(cls, artists, labels, is_compilation):
        triples = set()
        iterator = itertools.product(artists, labels)
        if is_compilation:
            role = 'Compiled On'
        else:
            role = 'Released On'
        for artist, label in iterator:
            triples.add((artist, role, label))
        return triples

    @classmethod
    def get_random(cls, roles=None):
        n = random.random()
        where_clause = (cls.random > n)
        if roles:
            where_clause &= (cls.role.in_(roles))
        query = cls.select().where(where_clause).order_by(cls.random).limit(1)
        print('Query:', query)
        while not query.count():
            n = random.random()
            where_clause = (cls.random > n)
            if roles:
                where_clause &= (cls.role.in_(roles))
            query = cls.select().where(where_clause).order_by(cls.random).limit(1)
            print('Query:', query)
        return query.get()

    @classmethod
    def get_release_setup(cls, release):
        is_compilation = False
        artists = set(
            (cls.EntityType.ARTIST, _['id'])
            for _ in release.artists
            )
        labels = set(
            (cls.EntityType.LABEL, _.get('id'))
            for _ in release.labels
            if _.get('id')
            )
        if len(artists) == 1 and release.artists[0]['name'] == 'Various':
            is_compilation = True
            artists.clear()
            for track in release.tracklist:
                artists.update(
                    (cls.EntityType.ARTIST, _['id'])
                    for _ in track.get('artists', ())
                    )
        #for format_ in release.formats:
        #    for description in format_.get('descriptions', ()):
        #        if description == 'Compilation':
        #            is_compilation = True
        #            break
        return artists, labels, is_compilation

    @classmethod
    def from_triples(cls, triples, release=None):
        relations = []
        for entity_one, role, entity_two in triples:
            entity_one_type, entity_one_id = entity_one
            entity_two_type, entity_two_id = entity_two
            relation = dict(
                entity_one_id=entity_one_id,
                entity_one_type=entity_one_type,
                entity_two_id=entity_two_id,
                entity_two_type=entity_two_type,
                role=role,
                )
            if release is not None:
                relation['release_id'] = release.id
                if release.release_date is not None:
                    relation['year'] = release.release_date.year
            relations.append(relation)
        return relations

    @classmethod
    def search(cls, entity_id, entity_type=1, roles=None, year=None, query_only=False):
        where_clause = (
            (cls.entity_one_id == entity_id) &
            (cls.entity_one_type == entity_type)
            )
        where_clause |= (
            (cls.entity_two_id == entity_id) &
            (cls.entity_two_type == entity_type)
            )
        if roles:
            where_clause &= (cls.role.in_(roles))
        if year is not None:
            year_clause = cls.year.is_null(True)
            if isinstance(year, int):
                year_clause |= cls.year == year
            else:
                year_clause |= cls.year.between(year[0], year[1])
            where_clause &= year_clause
        query = cls.select().where(where_clause)
        if query_only:
            return query
        return list(query)

    @classmethod
    def search_multi(cls, entity_keys, roles=None):
        assert entity_keys
        artist_ids, label_ids = [], []
        for entity_type, entity_id in entity_keys:
            if entity_type == 1:
                artist_ids.append(entity_id)
            elif entity_type == 2:
                label_ids.append(entity_id)
        if artist_ids:
            artist_where_clause = (
                ((cls.entity_one_type == 1) & (cls.entity_one_id.in_(artist_ids))) |
                ((cls.entity_two_type == 1) & (cls.entity_two_id.in_(artist_ids)))
                )
        if label_ids:
            label_where_clause = (
                ((cls.entity_one_type == 2) & (cls.entity_one_id.in_(label_ids))) |
                ((cls.entity_two_type == 2) & (cls.entity_two_id.in_(label_ids)))
                )
        if artist_ids and label_ids:
            where_clause = artist_where_clause | label_where_clause
        elif artist_ids:
            where_clause = artist_where_clause
        elif label_ids:
            where_clause = label_where_clause
        if roles:
            where_clause &= (cls.role.in_(roles))
        query = cls.select().where(where_clause)
        relations = {}
        for relation in query:
            relations[relation.link_key] = relation
        return relations

    @classmethod
    def search_bimulti(cls, lh_entities, rh_entities, roles=None, year=None, verbose=True):
        def build_query(lh_type, lh_ids, rh_type, rh_ids):
            where_clause = cls.entity_one_type == lh_type
            where_clause &= cls.entity_two_type == rh_type
            where_clause &= cls.entity_one_id.in_(lh_ids)
            where_clause &= cls.entity_two_id.in_(rh_ids)
            if roles:
                where_clause &= cls.role.in_(roles)
            if year is not None:
                year_clause = cls.year.is_null(True)
                if isinstance(year, int):
                    year_clause |= cls.year == year
                else:
                    year_clause |= cls.year.between(year[0], year[1])
                where_clause &= year_clause
            query = cls.select().where(where_clause)
            return query
        lh_artist_ids = []
        lh_label_ids = []
        rh_artist_ids = []
        rh_label_ids = []
        for entity_type, entity_id in lh_entities:
            if entity_type == 1:
                lh_artist_ids.append(entity_id)
            else:
                lh_label_ids.append(entity_id)
        for entity_type, entity_id in rh_entities:
            if entity_type == 1:
                rh_artist_ids.append(entity_id)
            else:
                rh_label_ids.append(entity_id)
        queries = []
        if lh_artist_ids:
            lh_type, lh_ids = 1, lh_artist_ids
            if rh_artist_ids:
                rh_type, rh_ids = 1, rh_artist_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                queries.append(query)
            if rh_label_ids:
                rh_type, rh_ids = 2, rh_label_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                queries.append(query)
        if lh_label_ids:
            lh_type, lh_ids = 2, lh_label_ids
            if rh_artist_ids:
                rh_type, rh_ids = 1, rh_artist_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                queries.append(query)
            if rh_label_ids:
                rh_type, rh_ids = 2, rh_label_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                queries.append(query)
        relations = []
        for query in queries:
            #print(query)
            relations.extend(query)
        relations = {
            relation.link_key: relation
            for relation in relations
            }
        return relations

    ### PUBLIC PROPERTIES ###

    @property
    def entity_one_key(self):
        return (self.entity_one_type, self.entity_one_id)

    @property
    def entity_two_key(self):
        return (self.entity_two_type, self.entity_two_id)

    @property
    def json_entity_one_key(self):
        if self.entity_one_type == 1:
            return 'artist-{}'.format(self.entity_one_id)
        elif self.entity_one_type == 2:
            return 'label-{}'.format(self.entity_one_id)
        raise ValueError(self.entity_one_key)

    @property
    def json_entity_two_key(self):
        if self.entity_two_type == 1:
            return 'artist-{}'.format(self.entity_two_id)
        elif self.entity_two_type == 2:
            return 'label-{}'.format(self.entity_two_id)
        raise ValueError(self.entity_two_key)

    @property
    def link_key(self):
        source = self.json_entity_one_key
        target = self.json_entity_two_key
        role = self.word_pattern.sub('-', self.role).lower()
        pieces = [
            source,
            role,
            target,
            ]
        return '-'.join(str(_) for _ in pieces)
