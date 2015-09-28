# -*- encoding: utf-8 -*-
import random
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
    def get_random(cls, role_names=None):
        n = random.random()
        where_clause = (cls.random > n)
        if role_names:
            where_clause &= cls.role_name.in_(role_names)
        return cls.select().where(where_clause).order_by(cls.random).get()

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
    def search_multi(cls, entities, role_names=None, year=None, verbose=True):
        def build_where_clause(entity_ids, entity_type):
            where_clause = (
                (cls.entity_one_type == entity_type) &
                (cls.entity_one_id.in_(entity_ids))
                ) | (
                (cls.entity_two_type == entity_type) &
                (cls.entity_two_id.in_(entity_ids))
                )
            if role_names:
                where_clause &= cls.role_name.in_(role_names)
            if year is not None:
                year_clause = cls.year.is_null(True)
                if isinstance(year, int):
                    year_clause |= cls.year == year
                else:
                    year_clause |= cls.year.between(year[0], year[1])
                where_clause &= year_clause
            return where_clause
        if verbose:
            print('            Searching... {}'.format(len(entities)))
        artist_ids = []
        label_ids = []
        for entity_type, entity_id in entities:
            if entity_type == 1:
                artist_ids.append(entity_id)
            else:
                label_ids.append(entity_id)
        relations = []
        if artist_ids:
            artist_where_clause = build_where_clause(artist_ids, 1)
            artist_query = cls.select().where(artist_where_clause)
            relations.extend(list(artist_query))
        if label_ids:
            label_where_clause = build_where_clause(label_ids, 2)
            label_query = cls.select().where(label_where_clause)
            relations.extend(list(label_query))
        return relations

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