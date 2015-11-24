import peewee
import unittest
from playhouse import test_utils
from playhouse import pool
from discograph.app import app


test_database = pool.PooledPostgresqlExtDatabase(
    'test_discograph',
    max_connections=16,
    host='127.0.0.1',
    user=app.config['POSTGRESQL_USERNAME'],
    password=app.config['POSTGRESQL_PASSWORD'],
    )


class DiscographTestCase(unittest.TestCase):

    def run(self, result=None):
        import discograph
        discograph.Bootstrapper.is_test = True
        models = (
            discograph.PostgresEntity,
            discograph.PostgresMaster,
            discograph.PostgresModel,
            discograph.PostgresRelation,
            discograph.PostgresRelease,
            )
        with test_utils.test_database(test_database, models):
            super(DiscographTestCase, self).run(result)
