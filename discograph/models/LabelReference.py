import mongoengine
from discograph.models.Model import Model


class LabelReference(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    discogs_id = mongoengine.IntField()
    name = mongoengine.StringField()

    ### PUBLIC METHODS ###

    @classmethod
    def from_parent_label(cls, parent_label):
        if parent_label is None or parent_label.text is None:
            return None
        name = parent_label.text.strip()
        if not name:
            return None
        return cls(name=name)

    @classmethod
    def from_sublabels(cls, sublabels):
        result = []
        if sublabels is None or not len(sublabels):
            return result
        for sublabel in sublabels:
            name = sublabel.text
            if name is None:
                continue
            name = name.strip()
            if not name:
                continue
            result.append(cls(name=name))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def label(self):
        from discograph import models
        return models.Label.objects.get(discogs_id=self.discogs_id)