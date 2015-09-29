# -*- encoding: utf-8 -*-
from discograph.library.SQLEntity import SQLEntity
from playhouse import sqlite_ext


class SQLFTSEntity(SQLEntity, sqlite_ext.FTSModel):
    pass
