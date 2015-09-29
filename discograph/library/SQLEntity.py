# -*- encoding: utf-8 -*-
import random
import peewee
from discograph.library.SQLModel import SQLModel


class SQLEntity(SQLModel):

    ### PEEWEE FIELDS ###

    entity_id = peewee.IntegerField()
    entity_type = peewee.IntegerField()
    name = peewee.TextField(null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'entity'
        indexes = (
            (('entity_id', 'entity_type'), True),
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _populate_from_mongo(cls, mongo_class, entity_type):
        query = mongo_class.objects().no_cache().timeout(False)
        query = query.only('discogs_id', 'name')
        count = query.count()
        rows = []
        for i, mongo_document in enumerate(query, 1):
            if mongo_document.discogs_id and mongo_document.name:
                rows.append(dict(
                    entity_id=mongo_document.discogs_id,
                    entity_type=entity_type,
                    name=mongo_document.name,
                    random=random.random(),
                    ))
            if len(rows) == 100:
                cls.insert_many(rows).execute()
                rows = []
                print('Processing {}s... {} of {} [{:.3f}%]'.format(
                    mongo_class.__name__.lower(),
                    i,
                    count,
                    (float(i) / count) * 100),
                    )
        if rows:
            cls.insert_many(rows).execute()
            print('Processing {}s... {} of {} [{:.3f}%]'.format(
                mongo_class.__name__.lower(),
                i,
                count,
                (float(i) / count) * 100),
                )

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        import discograph
        discograph.SQLFTSEntity.drop_table(True)
        discograph.SQLEntity.drop_table(True)
        discograph.SQLEntity.create_table()
        discograph.SQLFTSEntity.create_table(
            content=discograph.SQLEntity,
            tokenize='porter',
            )
        cls._populate_from_mongo(discograph.Artist, 1)
        cls._populate_from_mongo(discograph.Label, 2)
        discograph.SQLFTSEntity.rebuild()
        discograph.SQLFTSEntity.optimize()

    @classmethod
    def from_artist_id(cls, artist_id):
        return cls.select().where(
            (cls.entity_id == artist_id) & (cls.entity_type == 1)
            ).get()

    @classmethod
    def from_label_id(cls, label_id):
        return cls.select().where(
            (cls.entity_id == label_id) & (cls.entity_type == 2)
            ).get()

    def get_relations(self, role_names=None):
        from discograph.library.SQLRelation import SQLRelation
        return SQLRelation.search(
            entity_id=self.entity_id,
            entity_type=self.entity_type,
            role_names=role_names,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def entity_type_name(self):
        if self.entity_type == 1:
            return 'artist'
        elif self.entity_type == 2:
            return 'label'
        raise ValueError