# -*- encoding: utf-8 -*-
import peewee
from playhouse import postgres_ext
from discograph.library.Bootstrapper import Bootstrapper
from discograph.library.postgres.PostgresModel import PostgresModel


class PostgresRelease(PostgresModel):

    ### CLASS VARIABLES ###

    _artists_mapping = {}

    _companies_mapping = {}

    _tracks_mapping = {}

    ### PEEWEE FIELDS ###

    id = peewee.IntegerField(primary_key=True)
    artists = postgres_ext.BinaryJSONField(null=True)
    companies = postgres_ext.BinaryJSONField(null=True)
    country = peewee.TextField(null=True)
    extra_artists = postgres_ext.BinaryJSONField(null=True)
    formats = postgres_ext.BinaryJSONField(null=True)
    genres = postgres_ext.ArrayField(peewee.TextField, null=True)
    identifiers = postgres_ext.BinaryJSONField(null=True)
    labels = postgres_ext.BinaryJSONField(null=True)
    master_id = peewee.IntegerField(null=True)
    notes = peewee.TextField(null=True)
    release_date = peewee.DateTimeField(null=True)
    styles = postgres_ext.ArrayField(peewee.TextField, null=True)
    title = peewee.TextField()
    tracklist = postgres_ext.BinaryJSONField(null=True)

    ### PEEWEE META ###

    class Meta:
        db_table = 'releases'

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
            xml_tag='release',
            name_attr='title',
            skip_without=['title'],
            )

    @classmethod
    def bootstrap_pass_two(cls):
        PostgresModel.bootstrap_pass_two(cls, 'title')

    @classmethod
    def element_to_artist_credits(cls, element):
        result = []
        if element is None or not len(element):
            return result
        for subelement in element:
            data = cls.tags_to_fields(
                subelement,
                ignore_none=True,
                mapping=cls._artists_mapping,
                )
            result.append(data)
        return result

    @classmethod
    def element_to_company_credits(cls, element):
        result = []
        if element is None or not len(element):
            return result
        for subelement in element:
            data = cls.tags_to_fields(
                subelement,
                ignore_none=True,
                mapping=cls._companies_mapping,
                )
            result.append(data)
        return result

    @classmethod
    def element_to_formats(cls, element):
        result = []
        if element is None or not len(element):
            return result
        for subelement in element:
            document = {
                'name': subelement.get('name'),
                'quantity': subelement.get('qty'),
                }
            if subelement.get('text'):
                document['text'] = subelement.get('text')
            if len(subelement):
                subelement = subelement[0]
                descriptions = Bootstrapper.element_to_strings(subelement)
                document['descriptions'] = descriptions
            result.append(document)
        return result

    @classmethod
    def element_to_identifiers(cls, element):
        result = []
        if element is None or not len(element):
            return result
        for subelement in element:
            data = {
                'description': subelement.get('description'),
                'type': subelement.get('type'),
                'value': subelement.get('value'),
                }
            result.append(data)
        return result

    @classmethod
    def element_to_label_credits(cls, element):
        result = []
        if element is None or not len(element):
            return result
        for subelement in element:
            data = {
                'catalog_number': subelement.get('catno'),
                'name': subelement.get('name'),
                }
            result.append(data)
        return result

    @classmethod
    def element_to_roles(cls, element):
        def from_text(text):
            name = ''
            current_buffer = ''
            details = []
            had_detail = False
            bracket_depth = 0
            for character in text:
                if character == '[':
                    bracket_depth += 1
                    if bracket_depth == 1 and not had_detail:
                        name = current_buffer
                        current_buffer = ''
                        had_detail = True
                    elif 1 < bracket_depth:
                        current_buffer += character
                elif character == ']':
                    bracket_depth -= 1
                    if not bracket_depth:
                        details.append(current_buffer)
                        current_buffer = ''
                    else:
                        current_buffer += character
                else:
                    current_buffer += character
            if current_buffer and not had_detail:
                name = current_buffer
            name = name.strip()
            detail = ', '.join(_.strip() for _ in details)
            result = {'name': name}
            if detail:
                result['detail'] = detail
            return result
        credit_roles = []
        if element is None or not element.text:
            return credit_roles or None
        current_text = ''
        bracket_depth = 0
        for character in element.text:
            if character == '[':
                bracket_depth += 1
            elif character == ']':
                bracket_depth -= 1
            elif not bracket_depth and character == ',':
                current_text = current_text.strip()
                if current_text:
                    credit_roles.append(from_text(current_text))
                current_text = ''
                continue
            current_text += character
        current_text = current_text.strip()
        if current_text:
            credit_roles.append(from_text(current_text))
        return credit_roles or None

    @classmethod
    def element_to_tracks(cls, element):
        result = []
        if element is None or not len(element):
            return result
        for subelement in element:
            data = cls.tags_to_fields(
                subelement,
                ignore_none=True,
                mapping=cls._tracks_mapping,
                )
            result.append(data)
        return result

    @classmethod
    def from_element(cls, element):
        data = cls.tags_to_fields(element)
        data['id'] = int(element.get('id'))
        return cls(**data)

    def resolve_references(self, corpus, spuriously=False):
        import discograph
        changed = False
        spurious_id = 0
        for entry in self.labels:
            name = entry['name']
            entity_key = (2, name)
            if not spuriously:
                discograph.PostgresEntity.update_corpus(corpus, entity_key)
            if entity_key in corpus:
                entry['id'] = corpus[entity_key]
                changed = True
            elif spuriously:
                spurious_id -= 1
                corpus[entity_key] = spurious_id
                entry['id'] = corpus[entity_key]
                changed = True
        return changed


PostgresRelease._tags_to_fields_mapping = {
    'artists': ('artists', PostgresRelease.element_to_artist_credits),
    'companies': ('companies', PostgresRelease.element_to_company_credits),
    'country': ('country', Bootstrapper.element_to_string),
    'extraartists': ('extra_artists', PostgresRelease.element_to_artist_credits),
    'formats': ('formats', PostgresRelease.element_to_formats),
    'genres': ('genres', Bootstrapper.element_to_strings),
    'identifiers': ('identifiers', PostgresRelease.element_to_identifiers),
    'labels': ('labels', PostgresRelease.element_to_label_credits),
    'master_id': ('master_id', Bootstrapper.element_to_integer),
    'released': ('release_date', Bootstrapper.element_to_datetime),
    'styles': ('styles', Bootstrapper.element_to_strings),
    'title': ('title', Bootstrapper.element_to_string),
    'tracklist': ('tracklist', PostgresRelease.element_to_tracks),
    }


PostgresRelease._artists_mapping = {
    'id': ('id', Bootstrapper.element_to_integer),
    'name': ('name', Bootstrapper.element_to_string),
    'anv': ('anv', Bootstrapper.element_to_string),
    'join': ('join', Bootstrapper.element_to_string),
    'role': ('roles', PostgresRelease.element_to_roles),
    'tracks': ('tracks', Bootstrapper.element_to_string),
    }


PostgresRelease._companies_mapping = {
    'id': ('id', Bootstrapper.element_to_integer),
    'name': ('name', Bootstrapper.element_to_string),
    'catno': ('catalog_number', Bootstrapper.element_to_string),
    'entity_type': ('entity_type', Bootstrapper.element_to_integer),
    'entity_type_name': ('entity_type_name', Bootstrapper.element_to_string),
    }


PostgresRelease._tracks_mapping = {
    'position': ('position', Bootstrapper.element_to_string),
    'title': ('title', Bootstrapper.element_to_string),
    'duration': ('duration', Bootstrapper.element_to_string),
    'artists': ('artists', PostgresRelease.element_to_artist_credits),
    'extraartists': ('extra_artists', PostgresRelease.element_to_artist_credits),
    }