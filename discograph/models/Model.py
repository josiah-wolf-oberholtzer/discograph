from abjad.tools import systemtools


class Model(object):

    def __format__(self, format_specification=''):
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __repr__(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    @property
    def _storage_format_specification(self):
        keyword_argument_names = sorted(self._fields)
        if 'id' in keyword_argument_names:
            keyword_argument_names.remove('id')
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    @property
    def _repr_specification(self):
        return self._storage_format_specification