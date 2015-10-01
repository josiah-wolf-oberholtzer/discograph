# -*- encoding: utf-8 -*-
from discograph.library.sqlite.SqliteArtist import SqliteArtist
from playhouse import sqlite_ext


class SqliteFTSArtist(SqliteArtist, sqlite_ext.FTSModel):
    pass