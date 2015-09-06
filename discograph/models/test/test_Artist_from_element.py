# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from abjad import stringtools
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
        actual = bootstrap.Bootstrap.prettify(artist_element)
        expected = stringtools.normalize('''
            <?xml version="1.0" ?>
            <artist>
                <id>2</id>
                <name>Mr. James Barth &amp; A.D.</name>
                <realname>Cari Lekebusch &amp; Alexi Delano</realname>
                <profile/>
                <data_quality>Correct</data_quality>
                <namevariations>
                    <name>Mr Barth &amp; A.D.</name>
                    <name>MR JAMES BARTH &amp; A. D.</name>
                    <name>Mr. Barth &amp; A.D.</name>
                    <name>Mr. James Barth &amp; A. D.</name>
                </namevariations>
                <aliases>
                    <name>ADCL</name>
                    <name>Alexi Delano &amp; Cari Lekebusch</name>
                    <name>Crushed Insect &amp; The Sick Puppy</name>
                    <name>Puente Latino</name>
                    <name>Yakari &amp; Delano</name>
                </aliases>
                <members>
                    <id>26</id>
                    <name>Alexi Delano</name>
                    <id>27</id>
                    <name>Cari Lekebusch</name>
                </members>
            </artist>
            ''')
        assert actual.splitlines() == expected.splitlines()
        artist_document = models.Artist.from_element(artist_element)
        actual = format(artist_document)
        expected = stringtools.normalize('''
            discograph.models.Artist(
                aliases=[
                    discograph.models.ArtistReference(
                        name='ADCL',
                        ),
                    discograph.models.ArtistReference(
                        name='Alexi Delano & Cari Lekebusch',
                        ),
                    discograph.models.ArtistReference(
                        name='Crushed Insect & The Sick Puppy',
                        ),
                    discograph.models.ArtistReference(
                        name='Puente Latino',
                        ),
                    discograph.models.ArtistReference(
                        name='Yakari & Delano',
                        ),
                    ],
                discogs_id=2,
                members=[
                    discograph.models.ArtistReference(
                        discogs_id=26,
                        name='Alexi Delano',
                        ),
                    discograph.models.ArtistReference(
                        discogs_id=27,
                        name='Cari Lekebusch',
                        ),
                    ],
                name='Mr. James Barth & A.D.',
                name_variations=[
                    'Mr Barth & A.D.',
                    'MR JAMES BARTH & A. D.',
                    'Mr. Barth & A.D.',
                    'Mr. James Barth & A. D.',
                    ],
                real_name='Cari Lekebusch & Alexi Delano',
                )
            ''')
        assert actual == expected