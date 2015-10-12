# -*- encoding: utf-8 -*-
import peewee
from playhouse import gfk
from playhouse import postgres_ext
from discograph.library.postgres.PostgresRelease import PostgresRelease
from discograph.library.postgres.PostgresModel import PostgresModel


class PostgresRelation(PostgresModel):

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
                if document.master_id not in corpus:
                    where_clause = master_class.id == document.master_id
                    query = master_class.select().where(where_clause)
                    if query.count():
                        found = list(query)[0]
                        corpus[document.master_id] = found.main_release_id
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
        for alias in artist.aliases:
            if not alias['id']:
                continue
            alias = discograph.PostgresArtist(id=alias['id'])
            artist_one, artist_two = sorted(
                [artist, alias],
                key=lambda x: x.id,
                )
            entity_one = (discograph.PostgresArtist, artist_one.id)
            entity_two = (discograph.PostgresArtist, artist_two.id)
            triples.add((entity_one, role, entity_two))
        role = 'Member Of'
        for member in artist.members:
            if not member['id']:
                continue
            entity_one = (discograph.PostgresArtist, member['id'])
            entity_two = (discograph.PostgresArtist, artist['id'])
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
        pass

    @classmethod
    def from_triples(cls, triples, release=None):
        relations = []
        for entity_one, role, entity_two in triples:
            entity_one_class, entity_one_id = entity_one
            entity_one = entity_one_class(id=entity_one_id)
            entity_two_class, entity_two_id = entity_two
            entity_two = entity_two_class(id=entity_two_id)
            relation = dict(
                entity_one=entity_one,
                entity_two=entity_two,
                release=release,
                role=role,
                )
            relations.append(relation)
        return relations