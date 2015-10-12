# -*- encoding: utf-8 -*-
from __future__ import print_function
import peewee
from playhouse import postgres_ext
from discograph.library.Bootstrapper import Bootstrapper
from discograph.library.postgres.PostgresModel import PostgresModel


class PostgresArtist(PostgresModel):

    ### PEEWEE FIELDS ###

    id = peewee.IntegerField(primary_key=True)
    aliases = postgres_ext.BinaryJSONField(null=True)
    groups = postgres_ext.BinaryJSONField(null=True)
    members = postgres_ext.BinaryJSONField(null=True)
    name = peewee.TextField(index=True)
    name_variations = postgres_ext.ArrayField(peewee.TextField, null=True)
    profile = peewee.TextField(null=True)
    real_name = peewee.TextField(null=True)
    urls = postgres_ext.ArrayField(peewee.TextField, null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'artists'

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
            xml_tag='artist',
            name_attr='name',
            skip_without=['name'],
            )

    @classmethod
    def bootstrap_pass_two(cls):
        PostgresModel.bootstrap_pass_two(cls, 'name')

    @classmethod
    def element_to_names(cls, names):
        result = {}
        if names is None or not len(names):
            return result
        for name in names:
            name = name.text
            if not name:
                continue
            result[name] = None
        return result

    @classmethod
    def element_to_names_and_ids(cls, names_and_ids):
        result = {}
        if names_and_ids is None or not len(names_and_ids):
            return result
        for i in range(0, len(names_and_ids), 2):
            discogs_id = int(names_and_ids[i].text)
            name = names_and_ids[i + 1].text
            result[name] = discogs_id
        return result

    @classmethod
    def from_element(cls, element):
        data = cls.tags_to_fields(element)
        return cls(**data)

    def resolve_references(self, corpus):
        changed = False
        if self.aliases:
            for name in self.aliases.keys():
                self.update_corpus(corpus, name)
                if name in corpus:
                    self.aliases[name] = corpus[name]
                    changed = True
        if self.members:
            for name in self.members.keys():
                self.update_corpus(corpus, name)
                if name in corpus:
                    self.members[name] = corpus[name]
                    changed = True
        if self.groups:
            for name in self.groups.keys():
                self.update_corpus(corpus, name)
                if name in corpus:
                    self.groups[name] = corpus[name]
                    changed = True
        return changed

    @classmethod
    def update_corpus(cls, corpus, name):
        import discograph
        artist_class = discograph.PostgresArtist
        if name in corpus:
            return
        query = artist_class.select().where(artist_class.name == name)
        query = query.limit(1)
        found = list(query)
        if found:
            corpus[name] = found[0].id


PostgresArtist._tags_to_fields_mapping = {
    'aliases': ('aliases', PostgresArtist.element_to_names),
    'groups': ('groups', PostgresArtist.element_to_names),
    'id': ('id', Bootstrapper.element_to_integer),
    'members': ('members', PostgresArtist.element_to_names_and_ids),
    'name': ('name', Bootstrapper.element_to_string),
    'namevariations': ('name_variations', Bootstrapper.element_to_strings),
    'profile': ('profile', Bootstrapper.element_to_string),
    'realname': ('real_name', Bootstrapper.element_to_string),
    'urls': ('urls', Bootstrapper.element_to_strings),
    }