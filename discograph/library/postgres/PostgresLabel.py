# -*- encoding: utf-8 -*-
from __future__ import print_function
import peewee
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
        PostgresModel.bootstrap_pass_two(cls, 'name')

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

    def resolve_references(self, corpus):
        changed = False
        if self.sublabels:
            for name in self.sublabels.keys():
                self.update_corpus(corpus, name)
                if name in corpus:
                    self.sublabels[name] = corpus[name]
                    changed = True
        if self.parent_label:
            for name in self.parent_label.keys():
                self.update_corpus(corpus, name)
                if name in corpus:
                    self.parent_label[name] = corpus[name]
                    changed = True
        return changed

    @classmethod
    def update_corpus(cls, corpus, name):
        import discograph
        label_class = discograph.PostgresLabel
        if name in corpus:
            return
        query = label_class.select().where(label_class.name == name)
        query = query.limit(1)
        found = list(query)
        if found:
            corpus[name] = found[0].id


PostgresLabel._tags_to_fields_mapping = {
    'contact_info': ('contact_info', Bootstrapper.element_to_string),
    'id': ('id', Bootstrapper.element_to_integer),
    'name': ('name', Bootstrapper.element_to_string),
    'parentLabel': ('parent_label', PostgresLabel.element_to_parent_label),
    'profile': ('profile', Bootstrapper.element_to_string),
    'sublabels': ('sublabels', PostgresLabel.element_to_sublabels),
    'urls': ('urls', Bootstrapper.element_to_strings),
    }