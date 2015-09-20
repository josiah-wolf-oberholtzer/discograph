# -*- encoding: utf-8 -*-
import peewee
from discograph.models.SQLModel import SQLModel


class SQLLabel(SQLModel):
    name = peewee.CharField(index=True, null=True)

    class Meta:
        db_table = 'label'
