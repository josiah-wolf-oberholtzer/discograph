# -*- encoding: utf-8 -*-
import peewee
import random
from discograph.library.SQLModel import SQLModel


class SQLArtist(SQLModel):

    ### PEEWEE FIELDS ###

    name = peewee.TextField(index=True, null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'artist'

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        import discograph
        discograph.SQLFTSArtist.drop_table(True)
        discograph.SQLArtist.drop_table(True)
        discograph.SQLArtist.create_table()
        discograph.SQLFTSArtist.create_table(
            content=discograph.SQLArtist,
            tokenize='porter',
            )
        query = discograph.Artist.objects().no_cache().timeout(False)
        query = query.only('discogs_id', 'name')
        count = query.count()
        rows = []
        for i, mongo_document in enumerate(query, 1):
            if mongo_document.discogs_id and mongo_document.name:
                rows.append(dict(
                    id=mongo_document.discogs_id,
                    name=mongo_document.name,
                    random=random.random(),
                    ))
            if len(rows) == 100:
                discograph.SQLArtist.insert_many(rows).execute()
                rows = []
                print('Processing... {} of {} [{:.3f}%]'.format(
                    i, count, (float(i) / count) * 100))
        if rows:
            discograph.SQLArtist.insert_many(rows).execute()
            print('Processing... {} of {} [{:.3f}%]'.format(
                i, count, (float(i) / count) * 100))
        discograph.SQLFTSArtist.rebuild()
        discograph.SQLFTSArtist.optimize()

    def get_relations(self, role_names=None):
        from discograph.library.SQLRelation import SQLRelation
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

    ### PUBLIC PROPERTIES ###

    @property
    def discogs_id(self):
        return self.id