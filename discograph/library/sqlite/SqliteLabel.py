# -*- encoding: utf-8 -*-
import peewee
from discograph.library.sqlite.SqliteModel import SqliteModel


class SqliteLabel(SqliteModel):

    ### PEEWEE FIELDS ###

    name = peewee.CharField(index=True, null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'label'

    ### PUBLIC METHODS ###

    def get_relations(self, role_names=None):
        from discograph.library.sqlite.SqliteRelation import SqliteRelation
        return SqliteRelation.search(
            entity_id=self.id,
            entity_type=2,
            role_names=role_names,
            )

    @classmethod
    def from_id(cls, id):
        return cls.select().where(cls.id == id).get()

    @classmethod
    def from_name(cls, name):
        return cls.select().where(cls.name == name).get()

    @classmethod
    def search_by_name(cls, name):
        return list(cls.select().where(cls.name % '*{}*'.format(name)))

    ### PUBLIC PROPERTIES ###

    @property
    def discogs_id(self):
        return self.id