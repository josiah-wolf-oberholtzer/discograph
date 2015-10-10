# -*- encoding: utf-8 -*-
import peewee
#from playhouse import postgres_ext
from playhouse import gfk
from discograph.library.postgres.PostgresRelease import PostgresRelease
from discograph.library.postgres.PostgresModel import PostgresModel


class PostgresRelation(PostgresModel):

    ### PEEWEE FIELDS ###

    entity_two_id = peewee.IntegerField()
    entity_two_type = peewee.CharField()
    entity_two = gfk.GFKField('entity_two_type', 'entity_two_id')
    entity_two_id = peewee.IntegerField()
    entity_two_type = peewee.CharField()
    entity_two = gfk.GFKField('entity_two_type', 'entity_two_id')
    role = peewee.IntegerField()
    release_id = peewee.ForeignKeyField(
        PostgresRelease,
        related_name='relations',
        null=True,
        )

    ### PEEWEE META ###

    class Meta:
        pass