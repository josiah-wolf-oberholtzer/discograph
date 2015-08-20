# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from abjad import stringtools
from discograph import bootstrap
from discograph import models


class Test(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('discograph:test')

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
                    u\'ADCL\',
                    u\'Alexi Delano & Cari Lekebusch\',
                    u\'Crushed Insect & The Sick Puppy\',
                    u\'Puente Latino\',
                    u\'Yakari & Delano\',
                    ],
                discogs_id=2,
                has_been_scraped=True,
                members=[
                    discograph.models.Artist(
                        aliases=[
                            u\'A.D.1010\',
                            u\'ADNY\',
                            u\'Bob Brewthbaker\',
                            u\'G.O.L.\',
                            u\'Leiva\',
                            ],
                        discogs_id=26,
                        has_been_scraped=True,
                        members=[],
                        name=u\'Alexi Delano\',
                        name_variations=[
                            u\'A Delano\',
                            u\'A. D.\',
                            u\'A. Delano\',
                            u\'A.D\',
                            u\'A.D.\',
                            u\'A.Delano\',
                            u\'AD\',
                            u\'Alex Delano\',
                            u\'Alexei Delano\',
                            u\'Alexi "Adny" Delano\',
                            u\'Alexi Dolano\',
                            u\'Alexi V. Delano\',
                            u\'Delano\',
                            u\'Delano, Alexi\',
                            u\'DJ Alexi\',
                            u\'DJ Alexi Delano\',
                            ],
                        real_name=u\'Alexi Delano\',
                        ),
                    discograph.models.Artist(
                        aliases=[
                            u\'Agent Orange\',
                            u\'Braincell\',
                            u\'C-Blast\',
                            u\'Cerebus\',
                            u\'Crushed Insect\',
                            u\'DJ Mystiska K\',
                            u\'Fred\',
                            u\'Kari Pekka\',
                            u\'Magenta\',
                            u\'Mantis, The (2)\',
                            u\'Mentap\',
                            u\'Mr. James Barth\',
                            u\'Mystic Letter K\',
                            u\'Phunkey Rhythm Doctor\',
                            u\'Rotortype\',
                            u\'Rubberneck\',
                            u\'Shape Changer\',
                            u\'Sir Jeremy Augustus Hutley Of Granith Hall\',
                            u\'Szerementa Programs\',
                            u\'Vector\',
                            u\'Yakari\',
                            ],
                        discogs_id=27,
                        has_been_scraped=True,
                        members=[],
                        name=u\'Cari Lekebusch\',
                        name_variations=[
                            u\'C Lekebusch\',
                            u\'C-Blast\',
                            u\'C. Lekebusch\',
                            u\'C. Lekebush\',
                            u\'C.Lekebusch\',
                            u\'C.Lekebush\',
                            u\'Cari Le Kebusch\',
                            u\'Cari Leke Busch\',
                            u\'Cari Lekebusch den rykande B\\xf6nsyrsan\',
                            u\'Cari Lekebush\',
                            u\'Cari Lelebusch\',
                            u\'Carl Lekebusch\',
                            u\'Lekebusch\',
                            u\'Lekebusch Musik\',
                            ],
                        real_name=u\'Cari Lekebusch\',
                        ),
                    ],
                name=u\'Mr. James Barth & A.D.\',
                name_variations=[
                    u\'Mr Barth & A.D.\',
                    u\'MR JAMES BARTH & A. D.\',
                    u\'Mr. Barth & A.D.\',
                    u\'Mr. James Barth & A. D.\',
                    ],
                real_name=u\'Mr. James Barth & A.D.\',
                )
            ''')
        assert actual == expected