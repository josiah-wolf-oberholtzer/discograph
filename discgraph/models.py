import mongoengine



class Artist(mongoengine.Document):
    aliases = mongoengine.ListField(mongoengine.StringField())
    discogs_id = mongoengine.IntField(unique=True)
    groups = mongoengine.ListField(mongoengine.ReferenceField('Artist'))
    members = mongoengine.ListField(mongoengine.ReferenceField('Artist'))
    name = mongoengine.StringField()
    has_been_scraped = mongoengine.BooleanField()


class Label(mongoengine.Document):
    pass


class Release(mongoengine.Document):
    pass


class Master(mongoengine.Document):
    pass