# -*- encoding: utf-8 -*-
import itertools
import peewee
import random
from abjad.tools import datastructuretools
from discograph.library.postgres.PostgresModel import PostgresModel


class PostgresRelation(PostgresModel):

    ### CLASS VARIABLES ###

    class EntityType(datastructuretools.Enumeration):
        ARTIST = 1
        LABEL = 2

    aggregate_role_names = (
        'Compiled By',
        'Curated By',
        'DJ Mix',
        'Hosted By',
        'Presenter',
        )

    ### PEEWEE FIELDS ###

    entity_one_type = peewee.IntegerField()
    entity_one_id = peewee.IntegerField()
    entity_two_type = peewee.IntegerField()
    entity_two_id = peewee.IntegerField()
    role = peewee.CharField()
    release_id = peewee.IntegerField(default=-1)
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
            document = list(query)[0]
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
            document = list(query)[0]
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
        corpus = {}
        release_class = discograph.PostgresRelease
        master_class = discograph.PostgresMaster
        maximum_id = release_class.select(peewee.fn.Max(release_class.id)).scalar()
        for i in range(1, maximum_id + 1):
            query = release_class.select().where(release_class.id == i)
            if not query.count():
                continue
            document = list(query)[0]
            if document.master_id:
                # Attempt to add master_id:master.main_release_id to corpus.
                if document.master_id not in corpus:
                    where_clause = master_class.id == document.master_id
                    query = master_class.select().where(where_clause)
                    if query.count():
                        found = list(query)[0]
                        corpus[document.master_id] = found.main_release_id
                # Skip if this release is not the master's main release.
                if (
                    document.master_id in corpus and
                    document.master_id != corpus[document.master_id]
                    ):
                    continue
            print('(id:{}) {}'.format(
                document.id,
                document.title,
                ))
            relations = cls.from_release(document)
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
                role_name = role['name']
                if role_name not in discograph.CreditRole.all_credit_roles:
                    continue
                elif role_name in cls.aggregate_role_names:
                    if role_name not in aggregate_roles:
                        aggregate_roles[role_name] = []
                    aggregate_credit = (cls.EntityType.ARTIST, credit['id'])
                    aggregate_roles[role_name].append(aggregate_credit)
                    continue
                entity_one = (cls.EntityType.ARTIST, credit['id'])
                triples.add((entity_one, role_name, entity_two))
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
                for role in credit['roles']:
                    role_name = role['name']
                    if role_name not in discograph.CreditRole.all_credit_roles:
                        continue
                    entity_one = (cls.EntityType.ARTIST, credit['id'])
                    triples.add((entity_one, role_name, entity_two))
        for role_name, aggregate_artists in aggregate_roles.items():
            iterator = itertools.product(all_track_artists, aggregate_artists)
            for track_artist, aggregate_artist in iterator:
                entity_one = aggregate_artist
                entity_two = track_artist
                triples.add((entity_one, role_name, entity_two))
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
    def get_release_setup(cls, release):
        is_compilation = False
        artists = set(
            (cls.EntityType.ARTIST, _['id'])
            for _ in release.artists
            )
        labels = set(
            (cls.EntityType.LABEL, _['id'])
            for _ in release.labels
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