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
        print('A')
        cls.drop_table(True)
        print('B')
        cls.create_table()
        print('C')
        #database = cls._meta.database
        #database.set_autocommit(False)
        #with database.transaction():
        #    cls.bootstrap_pass_one()
        #with database.transaction():
        #    cls.bootstrap_pass_two()
        #with database.transaction():
        #    cls.bootstrap_pass_three()
        #database.set_autocommit(True)
        cls.bootstrap_pass_one()

    @classmethod
    def bootstrap_pass_one(cls):
        import discograph
        print('D')
        query = discograph.PostgresArtist.select()
        print('E')
        for i, artist in enumerate(postgres_ext.ServerSide(query)):
            print('(idx:{}) (id:{}) {}'.format(
                i,
                artist.id,
                artist.name,
                ))
            relations = cls.from_artist(artist)
            cls.insert_many(relations)

    @classmethod
    def bootstrap_pass_two(cls):
        import discograph
        query = discograph.PostgresLabel.select()
        for i, label in enumerate(query):
            print('(idx:{}) (id:{}) {}'.format(
                i,
                label.id,
                label.name,
                ))
            relations = cls.from_label(label)
            cls.insert_many(relations)

    @classmethod
    def bootstrap_pass_three(cls):
        pass

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