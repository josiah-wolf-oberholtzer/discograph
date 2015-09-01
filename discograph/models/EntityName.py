import mongoengine
from abjad.tools import datastructuretools
from discograph.models.Model import Model


class EntityName(Model, mongoengine.Document):

    ### CLASS VARIABLES ###

    class EntityType(datastructuretools.Enumeration):
        ARTIST = 1
        LABEL = 2

    ### MONGOENGINE FIELDS ###

    discogs_id = mongoengine.IntField(required=True)
    entity_type = mongoengine.IntField(required=True)
    name = mongoengine.StringField(required=True)

    ### MONGOENGINE META ###

    meta = {
        'indexes': [
            '#entity_type',
            '#name',
            '$name',
            'discogs_id',
            'name',
            ],
        }

    ### PUBLIC PROPERTIES ###

    @classmethod
    def bootstrap(cls):
        from discograph import models
        cls.drop_collection()
        for artist in models.Artist.objects:
            discogs_id = artist.discogs_id
            entity_type = cls.EntityType.ARTIST
            name = artist.name
            cls(
                discogs_id=discogs_id,
                entity_type=entity_type,
                name=name,
                ).save()
            print('[{}] {}: {}'.format(
                entity_type.name,
                discogs_id,
                name,
                ))
        for label in models.Label.objects:
            discogs_id = label.discogs_id
            entity_type = cls.EntityType.LABEL
            name = label.name
            cls(
                discogs_id=discogs_id,
                entity_type=entity_type,
                name=name,
                ).save
            print('[{}] {}: {}'.format(
                entity_type.name,
                discogs_id,
                name,
                ))