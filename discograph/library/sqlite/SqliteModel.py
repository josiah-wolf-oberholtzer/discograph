# -*- encoding: utf-8 -*-
import discograph
import os
import peewee
import random
from abjad.tools import systemtools
from playhouse import apsw_ext


database_path = os.path.join(
    discograph.__path__[0],
    'data',
    'discograph.sqlite',
    )
database = apsw_ext.APSWDatabase(
    database_path,
    pragmas=(
        ('journal_mode', 'WAL'),
        ('cache_size', 20000),
        ('mmap_size', 1024 * 1024 * 32),
        )
    )


class SqliteModel(peewee.Model):

    ### PEEWEE FIELDS ###

    random = peewee.FloatField(index=True)

    ### PEEWEE META ###

    class Meta:
        database = database

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __repr__(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        keyword_argument_names = sorted(self._data)
        for keyword_argument_name in keyword_argument_names[:]:
            value = getattr(self, keyword_argument_name)
            if isinstance(value, list) and not value:
                keyword_argument_names.remove(keyword_argument_name)
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    @property
    def _repr_specification(self):
        return self._storage_format_specification

    ### PUBLIC METHODS ###

    @classmethod
    def get_random(cls):
        n = random.random()
        return cls.select().where(cls.random > n).order_by(cls.random).get()