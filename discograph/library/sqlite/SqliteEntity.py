# -*- encoding: utf-8 -*-
import peewee
from discograph.library.sqlite.SqliteModel import SqliteModel


class SqliteEntity(SqliteModel):

    ### PEEWEE FIELDS ###

    name = peewee.TextField(null=True)
    entity_id = peewee.IntegerField()
    entity_type = peewee.IntegerField()

    ### PEEWEE META ###

    class Meta:
        db_table = 'entity'

    ### PUBLIC METHODS ###

    @classmethod
    def from_artist_id(cls, artist_id):
        where_clause = cls.entity_id == id
        where_clause &= cls.entity_type == 1
        return cls.select().where(where_clause).get()

    @classmethod
    def from_label_id(cls, label_id):
        where_clause = cls.entity_id == id
        where_clause &= cls.entity_type == 2
        return cls.select().where(where_clause).get()

    ### PUBLIC PROPERTIES ###

    @property
    def discogs_id(self):
        return self.id