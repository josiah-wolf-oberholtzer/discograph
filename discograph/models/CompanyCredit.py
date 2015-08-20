import mongoengine
from discograph.models.Model import Model


class CompanyCredit(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    catalog_number = mongoengine.StringField()
    company = mongoengine.ReferenceField('Label')
    entity_type = mongoengine.IntField()
    entity_type_name = mongoengine.StringField()

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        from discograph import models
        catalog_number = element.find('catno').text or None
        company_name = element.find('name').text
        company = models.Label.from_name(company_name)
        entity_type = int(element.find('entity_type').text)
        entity_type_name = element.find('entity_type_name').text
        document = cls(
            catalog_number=catalog_number,
            company=company,
            entity_type=entity_type,
            entity_type_name=entity_type_name,
            )
        return document