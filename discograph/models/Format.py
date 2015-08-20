import mongoengine
from discograph.models.Model import Model


class Format(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    descriptions = mongoengine.ListField(mongoengine.StringField())
    name = mongoengine.StringField()
    quantity = mongoengine.IntField()
    text = mongoengine.StringField()

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        name = element.attrib.get('name', None)
        quantity = int(element.attrib.get('qty', 1))
        text = element.attrib.get('text', None) or None
        descriptions = element.find('descriptions')
        if descriptions is not None and len(descriptions):
            descriptions = [_.text for _ in descriptions]
        else:
            descriptions = None
        format_document = cls(
            descriptions=descriptions,
            name=name,
            quantity=quantity,
            text=text,
            )
        return format_document