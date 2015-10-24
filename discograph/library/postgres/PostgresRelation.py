# -*- encoding: utf-8 -*-
import itertools
import peewee
import random
import multiprocessing
import re
import time
from abjad.tools import datastructuretools
from discograph.library.postgres.PostgresModel import PostgresModel


class PostgresRelation(PostgresModel):

    ### CLASS VARIABLES ###

    class EntityType(datastructuretools.Enumeration):
        ARTIST = 1
        LABEL = 2

    class BootstrapWorker(multiprocessing.Process):

        corpus = {}

        def __init__(self, queue):
            multiprocessing.Process.__init__(self)
            self.queue = queue

        def run(self):
            proc_name = self.name
            while True:
                task = self.queue.get()
                if task is None:
                    self.queue.task_done()
                    break
                PostgresRelation.bootstrap_pass_three_inner(
                    task,
                    self.corpus,
                    annotation=proc_name,
                    )
                self.queue.task_done()

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
    release_id = peewee.IntegerField(default=-1)
    role = peewee.CharField()
    year = peewee.IntegerField(default=-1)

    ### PEEWEE META ###

    class Meta:
        db_table = 'relations'
        indexes = (
            (('entity_one_type', 'entity_one_id', 'role', 'year'), False),
            (('entity_two_type', 'entity_two_id', 'role', 'year'), False),
            (('entity_one_type', 'entity_one_id',
              'entity_two_type', 'entity_two_id', 'role', 'year'), False),
            )
        primary_key = peewee.CompositeKey(
            'entity_one_type',
            'entity_one_id',
            'entity_two_type',
            'entity_two_id',
            'role',
            'release_id',
            'year',
            )

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        cls.drop_table(True)
        cls.create_table()
        cls.bootstrap_pass_one()
        cls.bootstrap_pass_two()
        cls.bootstrap_pass_three()

    @classmethod
    def bootstrap_pass_one(cls):
        import discograph
        model_class = discograph.PostgresArtist
        maximum_id = model_class.select(peewee.fn.Max(model_class.id)).scalar()
        for i in range(1, maximum_id + 1):
            query = model_class.select().where(model_class.id == i)
            if not query.count():
                continue
            document = query.get()
            print('(id:{}) {}'.format(
                document.id,
                document.name,
                ))
            relations = cls.from_artist(document)
            for relation in relations:
                relation['random'] = random.random()
                print('    {}-{} -> {!r} -> {}-{}'.format(
                    relation['entity_one_type'].name,
                    relation['entity_one_id'],
                    relation['role'],
                    relation['entity_two_type'].name,
                    relation['entity_two_id'],
                    ))
                cls.create_or_get(**relation)

    @classmethod
    def bootstrap_pass_two(cls):
        import discograph
        model_class = discograph.PostgresLabel
        maximum_id = model_class.select(peewee.fn.Max(model_class.id)).scalar()
        for i in range(1, maximum_id + 1):
            query = model_class.select().where(model_class.id == i)
            if not query.count():
                continue
            document = query.get()
            print('(id:{}) {}'.format(
                document.id,
                document.name,
                ))
            relations = cls.from_label(document)
            for relation in relations:
                relation['random'] = random.random()
                print('    {}-{} -> {!r} -> {}-{}'.format(
                    relation['entity_one_type'].name,
                    relation['entity_one_id'],
                    relation['role'],
                    relation['entity_two_type'].name,
                    relation['entity_two_id'],
                    ))
                cls.create_or_get(**relation)

    @classmethod
    def bootstrap_pass_three(cls):
        import discograph
        release_class = discograph.PostgresRelease
        maximum_id = release_class.select(peewee.fn.Max(release_class.id)).scalar()
        queue = multiprocessing.JoinableQueue()
        workers = [cls.BootstrapWorker(queue) for _ in range(4)]
        for worker in workers:
            worker.start()
        for release_id in range(1, maximum_id + 1):
            while not queue.empty():
                time.sleep(0.0001)
            queue.put(release_id)
        for worker in workers:
            queue.put(None)
        queue.join()
        queue.close()
        for worker in workers:
            worker.join()
        for worker in workers:
            worker.terminate()

    @classmethod
    def bootstrap_pass_three_inner(cls, release_id, corpus, annotation=''):
        import discograph
        database = cls._meta.database
        with database.execution_context(with_transaction=False):
            release_class = discograph.PostgresRelease
            master_class = discograph.PostgresMaster
            query = release_class.select().where(release_class.id == release_id)
            if not query.count():
                return
            document = query.get()
            if document.master_id:
                if document.master_id in corpus:
                    main_release_id = corpus[document.master_id]
                else:
                    where_clause = master_class.id == document.master_id
                    query = master_class.select().where(where_clause)
                    if query.count():
                        master = query.get()
                        corpus[document.master_id] = master.main_release_id
                        main_release_id = corpus[document.master_id]
                    else:
                        main_release_id = document.id
                if main_release_id != document.id:
                    print('[{}] (id:{}) [SKIPPED] {}'.format(
                        annotation,
                        document.id,
                        document.title,
                        ))
                    return
            relations = cls.from_release(document)
            print('[{}] (id:{})           [{}] {}'.format(
                annotation,
                document.id,
                len(relations),
                document.title,
                ))
            for relation in relations:
                relation['random'] = random.random()
                cls.create_or_get(**relation)

    @classmethod
    def from_artist(cls, artist):
        triples = set()
        role = 'Alias'
        if artist.aliases:
            for alias_name, alias_id in artist.aliases.items():
                if not alias_id:
                    continue
                id_one, id_two = sorted([artist.id, alias_id])
                entity_one = (cls.EntityType.ARTIST, id_one)
                entity_two = (cls.EntityType.ARTIST, id_two)
                triples.add((entity_one, role, entity_two))
        if artist.members:
            role = 'Member Of'
            for member_name, member_id in artist.members.items():
                if not member_id:
                    continue
                entity_one = (cls.EntityType.ARTIST, member_id)
                entity_two = (cls.EntityType.ARTIST, artist.id)
                triples.add((entity_one, role, entity_two))
        triples = (_ for _ in triples
            if all((_[0][1], _[1], _[2][1]))
            )
        key_function = lambda x: (x[0][1], x[1], x[2][1])
        triples = sorted(triples, key=key_function)
        relations = cls.from_triples(triples)
        return relations

    @classmethod
    def from_label(cls, label):
        triples = set()
        role = 'Sublabel Of'
        if label.sublabels:
            for sublabel_name, sublabel_id in label.sublabels.items():
                if not sublabel_id:
                    continue
                id_one, id_two = sublabel_id, label.id
                entity_one = (cls.EntityType.LABEL, id_one)
                entity_two = (cls.EntityType.LABEL, id_two)
                triples.add((entity_one, role, entity_two))
        if label.parent_label:
            for parent_label_name, parent_label_id in label.parent_label.items():
                if not parent_label_id:
                    continue
                id_one, id_two = label.id, parent_label_id
                entity_one = (cls.EntityType.LABEL, id_one)
                entity_two = (cls.EntityType.LABEL, id_two)
                triples.add((entity_one, role, entity_two))
        triples = (_ for _ in triples
            if all((_[0][1], _[1], _[2][1]))
            )
        key_function = lambda x: (x[0][1], x[1], x[2][1])
        triples = sorted(triples, key=key_function)
        relations = cls.from_triples(triples)
        return relations

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
        while not query.count():
            n = random.random()
            where_clause = (cls.random > n)
            if roles:
                where_clause &= (cls.role.in_(roles))
            query = cls.select().where(where_clause).order_by(cls.random).limit(1)
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
        for format_ in release.formats:
            for description in format_.get('descriptions', ()):
                if description == 'Compilation':
                    is_compilation = True
                    break
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
        relations = []
        if lh_artist_ids:
            lh_type, lh_ids = 1, lh_artist_ids
            if rh_artist_ids:
                rh_type, rh_ids = 1, rh_artist_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                relations.extend(list(query))
            if rh_label_ids:
                rh_type, rh_ids = 2, rh_label_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                relations.extend(list(query))
        if lh_label_ids:
            lh_type, lh_ids = 2, lh_label_ids
            if rh_artist_ids:
                rh_type, rh_ids = 1, rh_artist_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                relations.extend(list(query))
            if rh_label_ids:
                rh_type, rh_ids = 2, rh_label_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                relations.extend(list(query))
        return relations

    ### PUBLIC PROPERTIES ###

    @property
    def entity_one_key(self):
        return (self.entity_one_type, self.entity_one_id)

    @property
    def entity_two_key(self):
        return (self.entity_two_type, self.entity_two_id)

    @property
    def link_key(self):
        source_type, source_id = self.entity_one_key
        target_type, target_id = self.entity_two_key
        if source_type == 1:
            source_type = 'artist'
        else:
            source_type = 'label'
        if target_type == 1:
            target_type = 'artist'
        else:
            target_type = 'label'
        role = self.word_pattern.sub('-', self.role).lower()
        pieces = [
            source_type,
            source_id,
            role,
            target_type,
            target_id,
            ]
        return '-'.join(str(_) for _ in pieces)