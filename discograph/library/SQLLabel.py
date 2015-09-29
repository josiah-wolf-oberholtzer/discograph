# -*- encoding: utf-8 -*-
import peewee
import random
from discograph.library.SQLModel import SQLModel


class SQLLabel(SQLModel):

    ### PEEWEE FIELDS ###

    name = peewee.CharField(index=True, null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'label'

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        import discograph
        discograph.SQLLabel.drop_table(fail_silently=True)
        discograph.SQLLabel.create_table()
        query = discograph.Label.objects().no_cache().timeout(False)
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
                discograph.SQLLabel.insert_many(rows).execute()
                rows = []
                print('Processing... {} of {} [{:.3f}%]'.format(
                    i, count, (float(i) / count) * 100))
        if rows:
            discograph.SQLLabel.insert_many(rows).execute()
            print('Processing... {} of {} [{:.3f}%]'.format(
                i, count, (float(i) / count) * 100))

    def get_relations(self, role_names=None):
        from discograph.library.SQLRelation import SQLRelation
        return SQLRelation.search(
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