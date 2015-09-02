import mongoengine
from discograph.models.Model import Model


class ArtistReference(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    discogs_id = mongoengine.IntField()
    name = mongoengine.StringField()

    ### PUBLIC METHODS ###

    @classmethod
    def from_members(cls, members):
        result = []
        if members is None or not len(members):
            return result
        for i in range(0, len(members), 2):
            discogs_id = int(members[i].text)
            name = members[i + 1].text
            result.append(cls(discogs_id=discogs_id, name=name))
        return result

    @classmethod
    def from_names(cls, names):
        result = []
        if names is None or not len(names):
            return result
        for alias in names:
            name = alias.text
            if not name:
                continue
            result.append(cls(name=name))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def artist(self):
        from discograph import models
        return models.Artist.objects.get(discogs_id=self.discogs_id)