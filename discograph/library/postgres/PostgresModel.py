# -*- encoding: utf-8 -*-
import gzip
import peewee
import pprint
import random
import traceback
from abjad.tools import systemtools
from playhouse import gfk
from playhouse import postgres_ext
from discograph.library.Bootstrapper import Bootstrapper


database = postgres_ext.PostgresqlExtDatabase(
    'discograph',
    #server_side_cursors=True,
    user=None,
    )


class PostgresModel(gfk.Model):

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
        keyword_argument_names = sorted(self._meta.fields)
        #if 'id' in keyword_argument_names:
        #    keyword_argument_names.remove('id')
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
    def bootstrap_postgres_models(cls):
        import discograph
        discograph.PostgresArtist.bootstrap()
        discograph.PostgresLabel.bootstrap()
        discograph.PostgresRelease.bootstrap()
        discograph.PostgresRelation.bootstrap()

    @classmethod
    def bootstrap_pass_one(
        cls,
        model_class,
        xml_tag,
        xml_path,
        name_attr='name',
        skip_without=None,
        ):
        # Pass one.
        template = u'{} (Pass 1) (idx:{}) (id:{}) [{:.8f}]: {}'
        with gzip.GzipFile(xml_path, 'r') as file_pointer:
            iterator = Bootstrapper.iterparse(file_pointer, xml_tag)
            for i, element in enumerate(iterator):
                data = None
                try:
                    with systemtools.Timer(verbose=False) as timer:
                        data = model_class.tags_to_fields(element)
                        if skip_without:
                            if any(not data.get(_) for _ in skip_without):
                                continue
                        if element.get('id'):
                            data['id'] = element.get('id')
                        data['random'] = random.random()
                        document = model_class.create(**data)
                    message = template.format(
                        model_class.__name__.upper(),
                        i,
                        document.id,
                        timer.elapsed_time,
                        getattr(document, name_attr),
                        )
                    print(message)
                except peewee.DataError as e:
                    pprint.pprint(data)
                    traceback.print_exc()
                    raise(e)

    @staticmethod
    def connect():
        database.connect()

    @classmethod
    def get_random(cls):
        n = random.random()
        return cls.select().where(cls.random > n).order_by(cls.random).get()

    @classmethod
    def tags_to_fields(cls, element, ignore_none=None, mapping=None):
        data = {}
        mapping = mapping or cls._tags_to_fields_mapping
        for child_element in element:
            entry = mapping.get(child_element.tag, None)
            if entry is None:
                continue
            field_name, procedure = entry
            value = procedure(child_element)
            if ignore_none and value is None:
                continue
            data[field_name] = value
        return data