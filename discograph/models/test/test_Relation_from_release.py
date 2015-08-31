# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from discograph import bootstrap
from discograph import models


class Test(unittest.TestCase):

    database_name = 'discograph:test'

    def setUp(self):
        self.database = mongoengine.connect(self.database_name)

    def tearDown(self):
        self.database.drop_database(self.database_name)
        self.database.close()

    def test_01(self):
        iterator = bootstrap.Bootstrap.get_iterator('release')
        release_element = next(iterator)
        release_document = models.Release.from_element(release_element)
        relations = models.Relation.from_release(release_document)