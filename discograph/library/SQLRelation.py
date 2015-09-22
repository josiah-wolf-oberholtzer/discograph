# -*- encoding: utf-8 -*-
import peewee
from discograph.library.SQLModel import SQLModel


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
            query = cls.select().where(
                (
                    (cls.entity_one_id == entity_id) &
                    (cls.entity_one_type == entity_type)
                    ) | (
                    (cls.entity_two_id == entity_id) &
                    (cls.entity_two_type == entity_type)
                    )
                )
        else:
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

    @classmethod
    def search_multi(cls, entities, role_names=None, query_only=False):
        artist_ids = []
        label_ids = []
        for entity_type, entity_id in entities:
            if entity_type == 1:
                artist_ids.append(entity_id)
            else:
                label_ids.append(entity_id)
        artist_where_clause = (
            (cls.entity_one_type == 1) &
            (cls.entity_one_id.in_(artist_ids))
            ) | (
            (cls.entity_two_type == 1) &
            (cls.entity_two_id.in_(artist_ids))
            )
        if role_names:
            artist_where_clause &= (cls.role_name.in_(role_names))
        artist_query = cls.select().where(artist_where_clause)
        print('COUNT', len(entities))
        print(artist_query)
        label_where_clause = (
            (cls.entity_one_type == 1) &
            (cls.entity_one_id.in_(label_ids))
            ) | (
            (cls.entity_two_type == 1) &
            (cls.entity_two_id.in_(label_ids))
            )
        if role_names:
            label_where_clause &= (cls.role_name.in_(role_names))
        label_query = cls.select().where(label_where_clause)
        if query_only:
            return artist_query, label_query
        return list(_._data for _ in artist_query) + \
            list(_._data for _ in label_query)

    def get_entity_one(self):
        from discograph.library.SQLArtist import SQLArtist
        from discograph.library.SQLLabel import SQLLabel
        entity_id = self.entity_one_id
        entity_type = self.entity_one_type
        if entity_type == 1:
            return SQLArtist.from_id(entity_id)
        return SQLLabel.from_id(entity_id)

    def get_entity_two(self):
        from discograph.library.SQLArtist import SQLArtist
        from discograph.library.SQLLabel import SQLLabel
        entity_id = self.entity_two_id
        entity_type = self.entity_two_type
        if entity_type == 1:
            return SQLArtist.from_id(entity_id)
        return SQLLabel.from_id(entity_id)