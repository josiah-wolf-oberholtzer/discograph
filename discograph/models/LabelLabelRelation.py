import mongoengine
from discograph.models.Model import Model


class LabelLabelRelation(Model, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    parent_label = mongoengine.ReferenceField('Label')
    child_label = mongoengine.ReferenceField('Label')

    ### MONGOENGINE META ###

    meta = {
        'collection': 'relations',
        }