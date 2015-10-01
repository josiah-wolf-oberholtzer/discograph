# -*- encoding: utf-8 -*-
from abjad.tools import systemtools


class Model(object):

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
        keyword_argument_names = sorted(self._fields)
        if 'id' in keyword_argument_names:
            keyword_argument_names.remove('id')
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
    def from_elements(cls, element):
        if element is not None and len(element):
            return [cls.from_element(_) for _ in element]
        return None

    @classmethod
    def tags_to_fields(cls, element):
        data = {}
        for child_element in element:
            entry = cls._tags_to_fields_mapping.get(child_element.tag, None)
            if entry is None:
                continue
            field_name, procedure = entry
            data[field_name] = procedure(child_element)
        return data