# -*- encoding: utf-8 -*-
import peewee
from discograph.models.SQLModel import SQLModel


class SQLArtist(SQLModel):
    name = peewee.CharField(index=True, null=True)

    class Meta:
        db_table = 'artist'