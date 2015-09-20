# -*- encoding: utf-8 -*-
import peewee
from discograph.models.SQLModel import SQLModel


class SQLRelation(SQLModel):

    ### PEEWEE FIELDS ###

    entity_one_id = peewee.IntegerField()
    entity_one_type = peewee.IntegerField()
    entity_two_id = peewee.IntegerField()
    entity_two_type = peewee.IntegerField()
    release_id = peewee.IntegerField(null=True)
    role_name = peewee.CharField()
    year = peewee.IntegerField(null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'relation'
        indexes = (
            (('entity_one_id', 'entity_one_type', 'role_name', 'year'), False),
            (('entity_two_id', 'entity_two_type', 'role_name', 'year'), False),
            )

    ### PUBLIC METHODS ###

    @classmethod
    def search(cls, entity_id, entity_type=1, role_names=None, query_only=False):
        if not role_names:
            role_names = [
                'Alias',
                'Member Of',
                'Released On',
                'Sublabel Of',
                ]
        query = cls.select().where(
            (
                (cls.entity_one_id == entity_id) &
                (cls.entity_one_type == entity_type) &
                (cls.role_name.in_(role_names))
                ) | (
                (cls.entity_two_id == entity_id) &
                (cls.entity_two_type == entity_type) &
                (cls.role_name.in_(role_names))
                )
            )
        if query_only:
            return query
        return list(query)

    def get_entity_one(self):
        from discograph.models.SQLArtist import SQLArtist
        from discograph.models.SQLLabel import SQLLabel
        entity_id = self.entity_one_id
        entity_type = self.entity_one_type
        if entity_type == 1:
            return SQLArtist.from_id(entity_id)
        return SQLLabel.from_id(entity_id)

    def get_entity_two(self):
        from discograph.models.SQLArtist import SQLArtist
        from discograph.models.SQLLabel import SQLLabel
        entity_id = self.entity_two_id
        entity_type = self.entity_two_type
        if entity_type == 1:
            return SQLArtist.from_id(entity_id)
        return SQLLabel.from_id(entity_id)