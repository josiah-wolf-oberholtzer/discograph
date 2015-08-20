import mongoengine
from discograph.models.Model import Model


class Track(Model, mongoengine.EmbeddedDocument):

    ### MONGOENGINE FIELDS ###

    artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    duration = mongoengine.StringField()
    extra_artists = mongoengine.EmbeddedDocumentListField('ArtistCredit')
    position = mongoengine.StringField()
    title = mongoengine.StringField()

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        from discograph import models
        # artists
        artists = element.find('artists')
        if artists is not None and len(artists):
            artists = [models.ArtistCredit.from_element(_) for _ in artists]
        else:
            artists = None
        # duration
        duration = element.find('duration')
        if duration is not None:
            duration = duration.text
        # extra artists
        extra_artists = element.find('extraartists')
        if extra_artists is not None and len(extra_artists):
            extra_artists = [models.ArtistCredit.from_element(_) for _ in extra_artists]
        else:
            extra_artists = None
        # position
        position = element.find('position')
        if position is not None:
            position = position.text
        # title
        title = element.find('title')
        if title is not None:
            title = title.text
        # construct
        document = cls(
            artists=artists,
            duration=duration,
            extra_artists=extra_artists,
            position=position,
            title=title,
            )
        return document