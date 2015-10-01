# -*- encoding: utf-8 -*-
import mongoengine
from discograph.library.Model import Model


class Identifier(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    type_ = mongoengine.StringField()
    value = mongoengine.StringField()

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        type_ = element.attrib.get('type', None) or None
        value = element.attrib.get('value', None) or None
        return cls(
            type_=type_,
            value=value,
            )