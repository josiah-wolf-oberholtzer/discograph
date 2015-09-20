import discograph
import os
import peewee
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
from abjad.tools import systemtools


config_path = os.path.join(discograph.__path__[0], 'discograph.cfg')
config = ConfigParser()
config.read(config_path)


class SQLModel(peewee.Model):

    class Meta:
        database = peewee.MySQLDatabase(
            'discograph',
            user=config.get('mysql', 'username'),
            password=config.get('mysql', 'password'),
            )

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