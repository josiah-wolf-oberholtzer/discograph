# -*- encoding: utf-8 -*-
import json
import peewee


class JSONField(peewee.BlobField):

    def python_value(self, value):
        return json.loads(value.decode('utf-8'))

    def db_value(self, value):
        return json.dumps(value).encode('raw_unicode_escape')