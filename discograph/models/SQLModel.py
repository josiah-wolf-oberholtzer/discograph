# -*- encoding: utf-8 -*-
import discograph
import os
import peewee
import random
#try:
#    from configparser import ConfigParser
#except ImportError:
#    from ConfigParser import ConfigParser
from abjad.tools import systemtools


#config_path = os.path.join(discograph.__path__[0], 'discograph.cfg')
#config = ConfigParser()
#config.read(config_path)
#database = peewee.MySQLDatabase(
#    'discograph',
#    user=config.get('mysql', 'username'),
#    password=config.get('mysql', 'password'),
#    )
database_path = os.path.join(
    discograph.__path__[0],
    'data',
    'discograph.sqlite',
    )
database = peewee.SqliteDatabase(database_path, journal_mode='WAL')


class SQLModel(peewee.Model):

    ### PEEWEE FIELDS

    random = peewee.FloatField()

    ### PEEWEE META

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
    def randomize(cls):
        for obj in cls.select():
            obj.random = random.random()
            obj.save()
            print(obj)