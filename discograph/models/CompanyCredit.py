import mongoengine
from discograph.bootstrap import Bootstrap
from discograph.models.Model import Model


class CompanyCredit(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    catalog_number = mongoengine.StringField()
    name = mongoengine.StringField()
    entity_type = mongoengine.IntField()
    entity_type_name = mongoengine.StringField()

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        data = cls.tags_to_fields(element)
        document = cls(**data)
        return document


CompanyCredit._tags_to_fields_mapping = {
    'catno': ('catalog_number', Bootstrap.element_to_string),
    'name': ('name', Bootstrap.element_to_string),
    'entity_type': ('entity_type', Bootstrap.element_to_integer),
    'entity_type_name': ('entity_type_name', Bootstrap.element_to_string)
    }