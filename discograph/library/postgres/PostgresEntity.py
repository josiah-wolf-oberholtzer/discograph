# -*- encoding: utf-8 -*-
import peewee
from playhouse import postgres_ext
from discograph.library.postgres.PostgresModel import PostgresModel


class PostgresEntity(PostgresModel):

    ### PEEWEE FIELDS ###

    entity_id = peewee.IntegerField()
    entity_type = peewee.IntegerField()
    name = peewee.TextField(index=True)
    relation_counts = postgres_ext.BinaryJSONField()
    metadata = postgres_ext.BinaryJSONField()
    entities = postgres_ext.BinaryJSONField()

    ### PEEWEE META ###

    class Meta:
        db_table = 'entities'
        primary_key = peewee.CompositeKey('entity_type', 'entity_id')

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        cls.drop_table(True)
        cls.create_table()
        cls.bootstrap_pass_one()

    @classmethod
    def bootstrap_pass_one(cls):
        import discograph
        for relation in discograph.PostgresRelation.select():
            cls.upsert_from_relation(relation, lh=True)
            cls.upsert_from_relation(relation, lh=False)

    @classmethod
    def upsert_from_relation(cls, relation, lh=True):
        import discograph
        if lh:
            relation_entity = relation.entity_one
        else:
            relation_entity = relation.entity_two
        clause = cls.entity == relation_entity
        query = discograph.PostgresEntity.select().where(clause)
        found = list(query)
        if found:
            found = found[0]
        else:
            found = cls(
                entity=relation_entity,
                name=relation_entity.name,
                )
        if relation.role not in found.relation_counts:
            found.relation_counts[relation.role] = 0
        found.relation_counts[relation.role] += 1
        found.save()