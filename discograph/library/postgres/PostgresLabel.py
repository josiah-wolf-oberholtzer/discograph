# -*- encoding: utf-8 -*-
from __future__ import print_function
import peewee
from abjad.tools import systemtools
from playhouse import postgres_ext
from discograph.library.Bootstrapper import Bootstrapper
from discograph.library.postgres.PostgresModel import PostgresModel


class PostgresLabel(PostgresModel):

    ### PEEWEE FIELDS ###

    id = peewee.IntegerField(primary_key=True)
    contact_info = peewee.TextField(null=True)
    name = peewee.TextField(index=True)
    parent_label = postgres_ext.BinaryJSONField(null=True)
    profile = peewee.TextField(null=True)
    sublabels = postgres_ext.BinaryJSONField(null=True)
    urls = postgres_ext.ArrayField(peewee.TextField, null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'labels'

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        cls.drop_table(True)
        cls.create_table()
        cls.bootstrap_pass_one()
        cls.bootstrap_pass_two()

    @classmethod
    def bootstrap_pass_one(cls):
        PostgresModel.bootstrap_pass_one(
            model_class=cls,
            xml_tag='label',
            xml_path=Bootstrapper.labels_xml_path,
            name_attr='name',
            skip_without=['name'],
            )

    @classmethod
    def bootstrap_pass_two(cls):
        # Pass two.
        query = cls.select()
        for i, document in enumerate(query):
            with systemtools.Timer(verbose=False) as timer:
                changed = document.resolve_references()
            if not changed:
                message = u'{} [SKIPPED] (Pass 2) (idx:{}) (id:{}) [{:.8f}]: {}'.format(
                    cls.__name__.upper(),
                    i,
                    document.id,
                    timer.elapsed_time,
                    document.name,
                    )
                print(message)
                continue
            document.save()
            message = u'{}           (Pass 2) (idx:{}) (id:{}) [{:.8f}]: {}'.format(
                cls.__name__.upper(),
                i,
                document.id,
                timer.elapsed_time,
                document.name,
                )
            print(message)

    @classmethod
    def element_to_parent_label(cls, parent_label):
        result = {}
        if parent_label is None or parent_label.text is None:
            return result
        name = parent_label.text.strip()
        if not name:
            return result
        result[name] = None
        return result

    @classmethod
    def element_to_sublabels(cls, sublabels):
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

    @classmethod
    def from_element(cls, element):
        data = cls.tags_to_fields(element)
        return cls(**data)

    def resolve_references(self):
        changed = False
        if self.sublabels:
            for sublabel_name in self.sublabels.keys():
                query = self.select().where(type(self).name == sublabel_name)
                found = list(query)
                if not found:
                    continue
                changed = True
                sublabel = found[0]
                self.sublabels[sublabel_name] = sublabel.id
        if self.parent_label:
            for label_name in self.parent_label.keys():
                query = self.select().where(type(self).name == label_name)
                found = list(query)
                if not found:
                    continue
                changed = True
                parent_label = found[0]
                self.parent_label[label_name] = parent_label.id
        return changed


PostgresLabel._tags_to_fields_mapping = {
    'contact_info': ('contact_info', Bootstrapper.element_to_string),
    'id': ('id', Bootstrapper.element_to_integer),
    'name': ('name', Bootstrapper.element_to_string),
    'parentLabel': ('parent_label', PostgresLabel.element_to_parent_label),
    'profile': ('profile', Bootstrapper.element_to_string),
    'sublabels': ('sublabels', PostgresLabel.element_to_sublabels),
    'urls': ('urls', Bootstrapper.element_to_strings),
    }