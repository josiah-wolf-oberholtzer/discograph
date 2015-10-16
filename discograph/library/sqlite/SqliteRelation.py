# -*- encoding: utf-8 -*-
import peewee
import random
from discograph.library.sqlite.SqliteModel import SqliteModel
from playhouse import postgres_ext


class SqliteRelation(SqliteModel):

    ### PEEWEE FIELDS ###

    entity_one_id = peewee.IntegerField()
    entity_one_type = peewee.IntegerField()
    entity_two_id = peewee.IntegerField()
    entity_two_type = peewee.IntegerField()
    release_id = peewee.IntegerField(null=True)
    role = peewee.CharField()
    year = peewee.IntegerField(null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'relation'
        #indexes = (
        #    (('entity_one_id', 'entity_one_type', 'role', 'year'), False),
        #    (('entity_two_id', 'entity_two_type', 'role', 'year'), False),
        #    (('entity_one_type', 'entity_one_id',
        #      'entity_two_type', 'entity_two_id', 'role', 'year'), False),
        #    )
        primary_key = peewee.CompositeKey(
            'entity_one_type',
            'entity_one_id',
            'entity_two_type',
            'entity_two_id',
            'role',
            'release_id',
            'year',
            )

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        import discograph
        print('Dropping table.')
        discograph.SqliteRelation.drop_table(fail_silently=True)
        print('Creating table.')
        discograph.SqliteRelation.create_table()
        print('Building PostgreSQL query.')
        query = discograph.PostgresRelation.select()
        count = query.count()
        query = postgres_ext.ServerSide(query)
        print('Enumerating...')
        rows = []
        for i, document in enumerate(query):
            rows.append(dict(
                entity_one_id=document.entity_one_id,
                entity_one_type=document.entity_one_type,
                entity_two_id=document.entity_two_id,
                entity_two_type=document.entity_two_type,
                year=document.year,
                role=document.role,
                release_id=document.release_id,
                random=document.random,
                ))
            if len(rows) == 100:
                with cls._meta.database.atomic():
                    discograph.SqliteRelation.insert_many(rows).execute()
                rows = []
                print('Processing... {} of {} [{:.3f}%]'.format(
                    i, count, (float(i) / count) * 100))
        if rows:
            with cls._meta.database.atomic():
                discograph.SqliteRelation.insert_many(rows).execute()
            print('Processing... {} of {} [{:.3f}%]'.format(
                i, count, (float(i) / count) * 100))
        print('Creating indexes...')
        index_field_sequences = [
            ('entity_one_id', 'entity_one_type', 'role', 'year'),
            ('entity_two_id', 'entity_two_type', 'role', 'year'),
            ('entity_one_type', 'entity_one_id', 'entity_two_type', 'entity_two_id', 'role', 'year'),
            ]
        for index_field_sequence in index_field_sequences:
            cls._meta.database.create_index(cls, index_field_sequence)

    @classmethod
    def get_random(cls, roles=None):
        n = random.random()
        where_clause = (cls.random > n)
        if roles:
            where_clause &= (cls.role.in_(roles))
        query = cls.select().where(where_clause).order_by(cls.random).limit(1)
        while not query.count():
            n = random.random()
            where_clause = (cls.random > n)
            if roles:
                where_clause &= (cls.role.in_(roles))
            query = cls.select().where(where_clause).order_by(cls.random).limit(1)
        return query.get()

    @classmethod
    def search(cls, entity_id, entity_type=1, roles=None, year=None, query_only=False):
        where_clause = (
            (cls.entity_one_id == entity_id) &
            (cls.entity_one_type == entity_type)
            )
        where_clause |= (
            (cls.entity_two_id == entity_id) &
            (cls.entity_two_type == entity_type)
            )
        if roles:
            where_clause &= (cls.role.in_(roles))
        if year is not None:
            year_clause = cls.year.is_null(True)
            if isinstance(year, int):
                year_clause |= cls.year == year
            else:
                year_clause |= cls.year.between(year[0], year[1])
            where_clause &= year_clause
        query = cls.select().where(where_clause)
        if query_only:
            return query
        return list(query)

    @classmethod
    def search_multi(cls, entities, roles=None, year=None, verbose=True):
        def build_where_clause(entity_ids, entity_type):
            where_clause = (
                (cls.entity_one_type == entity_type) &
                (cls.entity_one_id.in_(entity_ids))
                ) | (
                (cls.entity_two_type == entity_type) &
                (cls.entity_two_id.in_(entity_ids))
                )
            if roles:
                where_clause &= cls.role.in_(roles)
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
            #print(artist_query)
            relations.extend(list(artist_query))
        if label_ids:
            label_where_clause = build_where_clause(label_ids, 2)
            label_query = cls.select().where(label_where_clause)
            #print(label_query)
            relations.extend(list(label_query))
        return relations

    @classmethod
    def search_bimulti(cls, lh_entities, rh_entities, roles=None, year=None, verbose=True):
        def build_query(lh_type, lh_ids, rh_type, rh_ids):
            where_clause = cls.entity_one_type == lh_type
            where_clause &= cls.entity_two_type == rh_type
            where_clause &= cls.entity_one_id.in_(lh_ids)
            where_clause &= cls.entity_two_id.in_(rh_ids)
            if roles:
                where_clause &= cls.role.in_(roles)
            if year is not None:
                year_clause = cls.year.is_null(True)
                if isinstance(year, int):
                    year_clause |= cls.year == year
                else:
                    year_clause |= cls.year.between(year[0], year[1])
                where_clause &= year_clause
            query = cls.select().where(where_clause)
            return query
        lh_artist_ids = []
        lh_label_ids = []
        rh_artist_ids = []
        rh_label_ids = []
        for entity_type, entity_id in lh_entities:
            if entity_type == 1:
                lh_artist_ids.append(entity_id)
            else:
                lh_label_ids.append(entity_id)
        for entity_type, entity_id in rh_entities:
            if entity_type == 1:
                rh_artist_ids.append(entity_id)
            else:
                rh_label_ids.append(entity_id)
        relations = []
        if lh_artist_ids:
            lh_type, lh_ids = 1, lh_artist_ids
            if rh_artist_ids:
                rh_type, rh_ids = 1, rh_artist_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                relations.extend(list(query))
            if rh_label_ids:
                rh_type, rh_ids = 2, rh_label_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                relations.extend(list(query))
        if lh_label_ids:
            lh_type, lh_ids = 2, lh_label_ids
            if rh_artist_ids:
                rh_type, rh_ids = 1, rh_artist_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                relations.extend(list(query))
            if rh_label_ids:
                rh_type, rh_ids = 2, rh_label_ids
                query = build_query(lh_type, lh_ids, rh_type, rh_ids)
                relations.extend(list(query))
        return relations