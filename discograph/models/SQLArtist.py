# -*- encoding: utf-8 -*-
import peewee
from discograph.models.SQLModel import SQLModel


class SQLArtist(SQLModel):

    ### PEEWEE FIELDS ###

    name = peewee.TextField(index=True, null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'artist'

    ### PUBLIC METHODS ###

    def get_relations(self, role_names=None):
        from discograph.models.SQLRelation import SQLRelation
        return SQLRelation.search(
            entity_id=self.id,
            entity_type=1,
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