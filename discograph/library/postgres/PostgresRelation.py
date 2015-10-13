# -*- encoding: utf-8 -*-
import itertools
import peewee
from playhouse import gfk
from discograph.library.postgres.PostgresRelease import PostgresRelease
from discograph.library.postgres.PostgresModel import PostgresModel


class PostgresRelation(PostgresModel):

    ### CLASS VARIABLES ###

    aggregate_role_names = (
        'Compiled By',
        'Curated By',
        'DJ Mix',
        'Hosted By',
        'Presenter',
        )

    ### PEEWEE FIELDS ###

    entity_one_type = peewee.CharField()
    entity_one_id = peewee.IntegerField()
    entity_one = gfk.GFKField('entity_one_type', 'entity_one_id')

    entity_two_type = peewee.CharField()
    entity_two_id = peewee.IntegerField()
    entity_two = gfk.GFKField('entity_two_type', 'entity_two_id')

    role = peewee.IntegerField()

    release_id = peewee.ForeignKeyField(
        PostgresRelease,
        related_name='relations',
        null=True,
        )

    year = peewee.IntegerField()

    ### PEEWEE META ###

    class Meta:
        db_table = 'relations'
        indexes = (
            (('entity_one_type', 'entity_one_id', 'role', 'year'), False),
            (('entity_two_type', 'entity_two_id', 'role', 'year'), False),
            (('entity_one_type', 'entity_one_id',
              'entity_two_type', 'entity_two_id', 'role', 'year'), False),
            )

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        cls.drop_table(True)
        cls.create_table()
        cls.bootstrap_pass_one()
        #cls.bootstrap_pass_two()
        #cls.bootstrap_pass_three()

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
            cls.insert_many(relations)

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
            cls.insert_many(relations)

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
                document.name,
                ))
            relations = cls.from_release(document)
            cls.insert_many(relations)

    @classmethod
    def from_artist(cls, artist):
        import discograph
        triples = set()
        role = 'Alias'
        for alias_name, alias_id in artist.aliases.items():
            if not alias_id:
                continue
            id_one, id_two = sorted([artist.id, alias_id])
            entity_one = (discograph.PostgresArtist, id_one)
            entity_two = (discograph.PostgresArtist, id_two)
            triples.add((entity_one, role, entity_two))
        role = 'Member Of'
        for member_name, member_id in artist.members.items():
            if not member_id:
                continue
            entity_one = (discograph.PostgresArtist, member_id)
            entity_two = (discograph.PostgresArtist, artist.id)
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
        import discograph
        triples = set()
        role = 'Sublabel Of'
        if label.sublabels:
            for sublabel_name, sublabel_id in label.sublabels.items():
                if not sublabel_id:
                    continue
                id_one, id_two = sublabel_id, label.id
                entity_one = (discograph.PostgresLabel, id_one)
                entity_two = (discograph.PostgresLabel, id_two)
                triples.add((entity_one, role, entity_two))
        if label.parent_label:
            for parent_label_name, parent_label_id in label.parent_label.items():
                if not parent_label_id:
                    continue
                id_one, id_two = label.id, parent_label_id
                entity_one = (discograph.PostgresLabel, id_one)
                entity_two = (discograph.PostgresLabel, id_two)
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
                    aggregate_credit = (discograph.PostgresArtist, credit['id'])
                    aggregate_roles[role_name].append(aggregate_credit)
                    continue
                entity_one = (discograph.PostgresArtist, credit['id'])
                triples.add((entity_one, role_name, entity_two))

        all_track_artists = set()
        for track in release.tracklist:
            track_artists = set(
                (discograph.PostgresArtist, _['id'])
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
                    entity_one = (discograph.PostgresArtist, credit['id'])
                    triples.add((entity_one, role_name, entity_two))

        for role_name, aggregate_artists in aggregate_roles.items():
            iterator = itertools.product(all_track_artists, aggregate_artists)
            for track_artist, aggregate_artist in iterator:
                #entity_one = (type(aggregate_artist), aggregate_artist.id)
                #entity_two = (type(track_artist), track_artist.id)
                entity_one = aggregate_artist
                entity_two = track_artist
                triples.add((entity_one, role_name, entity_two))

        triples = (_ for _ in triples
            if all((_[0][1], _[1], _[2][1]))
            )
        key_function = lambda x: (x[0][1], x[1], x[2][1])
        triples = sorted(triples, key=key_function)
        relations = cls.from_triples(triples)
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
        import discograph
        is_compilation = False
        artists = set(
            (discograph.PostgresArtist, _['id'])
            for _ in release.artists
            )
        labels = set(
            (discograph.PostgresLabel, _['id'])
            for _ in release.labels
            )
        if len(artists) == 1 and release.artists[0]['name'] == 'Various':
            is_compilation = True
            artists.clear()
            for track in release.tracklist:
                artists.update(
                    (discograph.PostgresArtist, _['id'])
                    for _ in track['artists']
                    )
        for format_ in release.formats:
            for description in format_['descriptions']:
                if description == 'Compilation':
                    is_compilation = True
                    break
        return artists, labels, is_compilation

    @classmethod
    def from_triples(cls, triples, release_id=None):
        relations = []
        for entity_one, role, entity_two in triples:
            entity_one_class, entity_one_id = entity_one
            entity_one = entity_one_class(id=entity_one_id)
            entity_two_class, entity_two_id = entity_two
            entity_two = entity_two_class(id=entity_two_id)
            relation = dict(
                entity_one=entity_one,
                entity_two=entity_two,
                role=role,
                )
            if release_id:
                relation['release_id'] = release_id
            relations.append(relation)
        return relations