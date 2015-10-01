# -*- encoding: utf-8 -*-
import mongoengine
from discograph.library.mongo.MongoModel import MongoModel


class ArtistReference(MongoModel, mongoengine.EmbeddedDocument):

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
        for name in names:
            name = name.text
            if not name:
                continue
            result.append(cls(name=name))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def artist(self):
        from discograph import library
        return library.Artist.objects.get(discogs_id=self.discogs_id)