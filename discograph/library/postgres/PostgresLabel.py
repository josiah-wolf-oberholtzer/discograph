# -*- encoding: utf-8 -*-
from __future__ import print_function
import gzip
import peewee
import pprint
import random
import traceback
from abjad.tools import systemtools
from playhouse import postgres_ext
from discograph.library.Bootstrapper import Bootstrapper
from discograph.library.postgres.PostgresModel import PostgresModel


class PostgresLabel(PostgresModel):

    ### PEEWEE FIELDS ###

    id = peewee.IntegerField(primary_key=True)
    contact_info = peewee.TextField(null=True)
    name = peewee.TextField(index=True)
    parent_label = postgres_ext.HStoreField(null=True)
    profile = peewee.TextField(null=True)
    sublabels = postgres_ext.HStoreField(null=True)
    urls = postgres_ext.ArrayField(peewee.TextField, null=True)

    ### PEEWEE META ###

    class Meta:
        pass

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        cls.drop_table(True)
        cls.create_table()
        cls.bootstrap_pass_one()

    @classmethod
    def bootstrap_pass_one(cls):
        # Pass one.
        labels_xml_path = Bootstrapper.labels_xml_path
        with gzip.GzipFile(labels_xml_path, 'r') as file_pointer:
            iterator = Bootstrapper.iterparse(file_pointer, 'label')
            #iterator = Bootstrapper.clean_elements(iterator)
            for i, element in enumerate(iterator):
                data = None
                try:
                    with systemtools.Timer(verbose=False) as timer:
                        data = cls.tags_to_fields(element)
                        data['random'] = random.random()
                        document = cls.create(**data)
                    message = u'{} (Pass 1) {} [{}]: {}'.format(
                        cls.__name__.upper(),
                        document.id,
                        timer.elapsed_time,
                        document.name,
                        )
                    print(message)
                except peewee.DataError as e:
                    print('!!!!!!!!!!!!!!!!!!!!!!!')
                    pprint.pprint(data)
                    traceback.print_exc()
                    raise(e)

    @classmethod
    def hstore_from_parent_label(cls, parent_label):
        result = {}
        if parent_label is None or parent_label.text is None:
            return result
        name = parent_label.text.strip()
        if not name:
            return result
        result[name] = None
        return result

    @classmethod
    def hstore_from_sublabels(cls, sublabels):
        result = {}
        if sublabels is None or not len(sublabels):
            return result
        for sublabel in sublabels:
            name = sublabel.text
            if name is None:
                continue
            name = name.strip()
            if not name:
                continue
            result[name] = None
        return result


PostgresLabel._tags_to_fields_mapping = {
    'contact_info': ('contact_info', Bootstrapper.element_to_string),
    'id': ('id', Bootstrapper.element_to_integer),
    'name': ('name', Bootstrapper.element_to_string),
    'parentLabel': ('parent_label', PostgresLabel.hstore_from_parent_label),
    'profile': ('profile', Bootstrapper.element_to_string),
    'sublabels': ('sublabels', PostgresLabel.hstore_from_sublabels),
    'urls': ('urls', Bootstrapper.element_to_strings),
    }