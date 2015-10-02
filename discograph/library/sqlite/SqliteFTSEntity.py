# -*- encoding: utf-8 -*-
from discograph.library.sqlite.SqliteEntity import SqliteEntity
from playhouse import sqlite_ext


class SqliteFTSEntity(SqliteEntity, sqlite_ext.FTSModel):

    class Meta:
        db_table = 'sqlftsentity'