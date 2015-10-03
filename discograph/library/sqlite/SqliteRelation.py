# -*- encoding: utf-8 -*-
import peewee
import random
from discograph.library.sqlite.SqliteModel import SqliteModel


class SqliteRelation(SqliteModel):

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

    @staticmethod
    def bootstrap():
        import discograph
        discograph.SqliteRelation.drop_table(fail_silently=True)
        discograph.SqliteRelation.create_table()
        count = discograph.Relation.objects.count()
        query = discograph.Relation._get_collection().find()
        rows = []
        for i, mongo_document in enumerate(query, 1):
            rows.append(dict(
                id=i,
                entity_one_id=mongo_document.get('entity_one_id'),
                entity_one_type=mongo_document.get('entity_one_type'),
                entity_two_id=mongo_document.get('entity_two_id'),
                entity_two_type=mongo_document.get('entity_two_type'),
                year=mongo_document.get('year'),
                release_id=mongo_document.get('release_id'),
                role_name=mongo_document.get('role_name'),
                random=random.random(),
                ))
            if mongo_document.get('role_name') not in ('Alias', 'Member Of'):
                break
            if len(rows) == 100:
                discograph.SqliteRelation.insert_many(rows).execute()
                rows = []
                print('Processing... {} of {} [{:.3f}%]'.format(
                    i, count, (float(i) / count) * 100))
        if rows:
            discograph.SqliteRelation.insert_many(rows).execute()
            print('Processing... {} of {} [{:.3f}%]'.format(
                i, count, (float(i) / count) * 100))

    @classmethod
    def get_random(cls, role_names=None):
        n = random.random()
        where_clause = (cls.random > n)
        if role_names:
            where_clause &= (cls.role_name.in_(role_names))
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