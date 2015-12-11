# -*- encoding: utf-8 -*-
import unittest
from playhouse import test_utils
from playhouse import pool
from discograph.app import app
from discograph.library.Bootstrapper import Bootstrapper
from discograph.library.PostgresEntity import PostgresEntity
from discograph.library.PostgresMaster import PostgresMaster
from discograph.library.PostgresModel import PostgresModel
from discograph.library.PostgresRelation import PostgresRelation
from discograph.library.PostgresRelease import PostgresRelease


class DiscographTestCase(unittest.TestCase):

    test_database = pool.PooledPostgresqlExtDatabase(
        'test_discograph',
        host='127.0.0.1',
        user=app.config['POSTGRESQL_USERNAME'],
        password=app.config['POSTGRESQL_PASSWORD'],
        )

    models = (
        PostgresEntity,
        PostgresMaster,
        PostgresModel,
        PostgresRelation,
        PostgresRelease,
        )

    @classmethod
    def setUpTestDB(cls):
        Bootstrapper.is_test = True
        with test_utils.test_database(
            cls.test_database,
            cls.models,
            create_tables=False,
            fail_silently=True,
            ):
            print(PostgresModel._meta.database.database)
            PostgresModel.bootstrap_postgres_models(pessimistic=True)

    def run(self, result=None):
        import discograph
        discograph.Bootstrapper.is_test = True
        with test_utils.test_database(
            self.test_database,
            self.models,
            create_tables=False,
            fail_silently=True,
            ):
            super(DiscographTestCase, self).run(result)
