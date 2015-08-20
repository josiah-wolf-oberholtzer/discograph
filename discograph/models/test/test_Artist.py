# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from abjad import stringtools
from discograph import bootstrap
from discograph import models


class Test(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('discograph:test')
        models.Artist.drop_collection()

    def test_01(self):
        iterator = bootstrap.get_iterator('artist')
        artist_element = next(iterator)
        artist_element = next(iterator)
        actual = bootstrap.prettify(artist_element)
        expected = stringtools.normalize(u'''
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
        expected = stringtools.normalize(u'''
            discograph.models.Artist(
                aliases=[
                    'ADCL',
                    'Alexi Delano & Cari Lekebusch',
                    'Crushed Insect & The Sick Puppy',
                    'Puente Latino',
                    'Yakari & Delano',
                    ],
                discogs_id=2,
                has_been_scraped=True,
                members=[
                    discograph.models.Artist(
                        aliases=[],
                        discogs_id=26,
                        has_been_scraped=False,
                        members=[],
                        name=u'Alexi Delano',
                        name_variations=[],
                        ),
                    discograph.models.Artist(
                        aliases=[],
                        discogs_id=27,
                        has_been_scraped=False,
                        members=[],
                        name=u'Cari Lekebusch',
                        name_variations=[],
                        ),
                    ],
                name=u'Mr. James Barth & A.D.',
                name_variations=[
                    'Mr Barth & A.D.',
                    'MR JAMES BARTH & A. D.',
                    'Mr. Barth & A.D.',
                    'Mr. James Barth & A. D.',
                    ],
                real_name='Mr. James Barth & A.D.',
                )
            ''')
        assert actual == expected