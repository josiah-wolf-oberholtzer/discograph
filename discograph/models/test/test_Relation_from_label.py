# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from abjad.tools import stringtools
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
        iterator = bootstrap.Bootstrap.get_iterator('label')
        label_element = next(iterator)
        label_element = next(iterator)
        label_element = next(iterator)
        print(bootstrap.Bootstrap.prettify(label_element))
        label_document = models.Label.from_element(label_element)
        relations = models.Relation.from_label(label_document)
        actual = '\n'.join(format(_) for _ in relations)
        expected = stringtools.normalize(r'''
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_name='Seasons Classics',
                entity_one_type=discograph.models.Relation.EntityType.LABEL,
                entity_two_id=3,
                entity_two_name='Seasons Recordings',
                entity_two_type=discograph.models.Relation.EntityType.LABEL,
                role_name='Sublabel Of',
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_name='Seasons Limited',
                entity_one_type=discograph.models.Relation.EntityType.LABEL,
                entity_two_id=3,
                entity_two_name='Seasons Recordings',
                entity_two_type=discograph.models.Relation.EntityType.LABEL,
                role_name='Sublabel Of',
                )
            ''')
        assert actual == expected