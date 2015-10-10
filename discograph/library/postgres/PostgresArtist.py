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
        pass

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        cls.drop_table(True)
        cls.create_table()
        cls.bootstrap_pass_one()
        cls.bootstrap_pass_two()

    @classmethod
    def bootstrap_pass_one(cls):
        # Pass one.
        artists_xml_path = Bootstrapper.artists_xml_path
        with gzip.GzipFile(artists_xml_path, 'r') as file_pointer:
            iterator = Bootstrapper.iterparse(file_pointer, 'artist')
            for i, element in enumerate(iterator):
                data = None
                try:
                    with systemtools.Timer(verbose=False) as timer:
                        data = cls.tags_to_fields(element)
                        if not data.get('name'):
                            continue
                        data['random'] = random.random()
                        document = cls.create(**data)
                    message = u'{} (Pass 1) {} [{:.8f}]: {}'.format(
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

    def resolve_references(self):
        model = type(self)
        changed = False
        if self.aliases:
            for alias_name in self.aliases.keys():
                query = model.select().where(model.name == alias_name)
                found = list(query)
                if not found:
                    continue
                changed = True
                alias = found[0]
                self.aliases[alias_name] = alias.id
        if self.members:
            for member_name in self.members.keys():
                query = model.select().where(model.name == member_name)
                found = list(query)
                if not found:
                    continue
                changed = True
                member = found[0]
                self.members[member_name] = member.id
        if self.groups:
            for group_name in self.groups.keys():
                query = model.select().where(model.name == group_name)
                found = list(query)
                if not found:
                    continue
                changed = True
                group = found[0]
                self.groups[group_name] = group.id
        return changed


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