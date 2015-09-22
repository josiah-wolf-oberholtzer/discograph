# -*- encoding: utf-8 -*-
from discograph.library.SQLArtist import SQLArtist
from playhouse import sqlite_ext


class SQLFTSArtist(SQLArtist, sqlite_ext.FTSModel):
    pass