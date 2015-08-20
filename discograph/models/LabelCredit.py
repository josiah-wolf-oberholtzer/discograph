import mongoengine
from discograph.models.Model import Model


class LabelCredit(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    catalog_number = mongoengine.StringField()
    label = mongoengine.ReferenceField('Label')

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        from discograph import models
        catalog_number = element.attrib.get('catno', None) or None
        label_name = element.attrib.get('name')
        label = models.Label.from_name(label_name)
        document = cls(
            catalog_number=catalog_number,
            label=label,
            )
        return document