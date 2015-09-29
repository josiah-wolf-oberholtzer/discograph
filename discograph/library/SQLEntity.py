# -*- encoding: utf-8 -*-
import random
import peewee
from discograph.library.SQLModel import SQLModel


class SQLEntity(SQLModel):

    ### PEEWEE FIELDS ###

    entity_id = peewee.IntField()
    entity_type = peewee.IntField()
    name = peewee.CharField(index=True, null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'entity'

    ### PUBLIC METHODS ###

    def get_relations(self, role_names=None):
        from discograph.library.SQLRelation import SQLRelation
        return SQLRelation.search(
            entity_id=self.entity_id,
            entity_type=self.entity_type,
            role_names=role_names,
            )

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
        query = discograph.Artist.objects().no_cache().timeout(False)
        query = query.only('discogs_id', 'name')
        count = query.count()
        rows = []
        for i, mongo_document in enumerate(query, 1):
            if mongo_document.discogs_id and mongo_document.name:
                rows.append(dict(
                    entity_id=mongo_document.discogs_id,
                    entity_type=1,
                    name=mongo_document.name,
                    random=random.random(),
                    ))
            if len(rows) == 100:
                discograph.SQLEntity.insert_many(rows).execute()
                rows = []
                print('Processing artists... {} of {} [{:.3f}%]'.format(
                    i, count, (float(i) / count) * 100))
        if rows:
            discograph.SQLEntity.insert_many(rows).execute()
            print('Processing artists... {} of {} [{:.3f}%]'.format(
                i, count, (float(i) / count) * 100))
        query = discograph.Label.objects().no_cache().timeout(False)
        query = query.only('discogs_id', 'name')
        count = query.count()
        rows = []
        for i, mongo_document in enumerate(query, 1):
            if mongo_document.discogs_id and mongo_document.name:
                rows.append(dict(
                    entity_id=mongo_document.discogs_id,
                    entity_type=1,
                    name=mongo_document.name,
                    random=random.random(),
                    ))
            if len(rows) == 100:
                discograph.SQLEntity.insert_many(rows).execute()
                rows = []
                print('Processing labels... {} of {} [{:.3f}%]'.format(
                    i, count, (float(i) / count) * 100))
        if rows:
            discograph.SQLEntity.insert_many(rows).execute()
            print('Processing labels... {} of {} [{:.3f}%]'.format(
                i, count, (float(i) / count) * 100))
        discograph.SQLFTSEntity.rebuild()
        discograph.SQLFTSEntity.optimize()

    ### PUBLIC PROPERTIES ###

    @property
    def entity_type_name(self):
        if self.entity_type == 1:
            return 'artist'
        elif self.entity_type == 2:
            return 'label'
        raise ValueError