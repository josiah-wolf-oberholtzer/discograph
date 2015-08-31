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
        iterator = bootstrap.Bootstrap.get_iterator('artist')
        artist_element = next(iterator)
        artist_element = next(iterator)
        artist_document = models.Artist.from_element(artist_element)
        for discogs_id, alias in enumerate(artist_document.aliases, 100000000):
            models.Artist(discogs_id=discogs_id, name=alias).save()
        relations = models.Relation.from_artist(artist_document)
        actual = '\n'.join(format(_) for _ in relations)
        expected = stringtools.normalize(r'''
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=2,
                entity_one_name='Mr. James Barth & A.D.',
                entity_two_id=100000000,
                entity_two_name='ADCL',
                role_name='Alias',
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=2,
                entity_one_name='Mr. James Barth & A.D.',
                entity_two_id=100000001,
                entity_two_name='Alexi Delano & Cari Lekebusch',
                role_name='Alias',
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=2,
                entity_one_name='Mr. James Barth & A.D.',
                entity_two_id=100000002,
                entity_two_name='Crushed Insect & The Sick Puppy',
                role_name='Alias',
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=2,
                entity_one_name='Mr. James Barth & A.D.',
                entity_two_id=100000003,
                entity_two_name='Puente Latino',
                role_name='Alias',
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=2,
                entity_one_name='Mr. James Barth & A.D.',
                entity_two_id=100000004,
                entity_two_name='Yakari & Delano',
                role_name='Alias',
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=26,
                entity_one_name='Alexi Delano',
                entity_two_id=2,
                entity_two_name='Mr. James Barth & A.D.',
                role_name='Member Of',
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=27,
                entity_one_name='Cari Lekebusch',
                entity_two_id=2,
                entity_two_name='Mr. James Barth & A.D.',
                role_name='Member Of',
                )
            ''')
        assert actual == expected