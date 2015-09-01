# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from abjad.tools import stringtools
from discograph import models
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree


class Test(unittest.TestCase):

    database_name = 'discograph:test'

    def setUp(self):
        self.database = mongoengine.connect(self.database_name)

    def tearDown(self):
        self.database.drop_database(self.database_name)
        self.database.close()

    def test_1(self):
        source = '''
            <artists>
                <artist>
                    <id>1</id>
                    <name>Persuader, The</name>
                    <anv/>
                    <join/>
                    <role/>
                    <tracks/>
                </artist>
            </artists>
            '''
        element = ElementTree.fromstring(source)
        artist_credits = models.ArtistCredit.from_elements(element)
        assert format(artist_credits[0]) == stringtools.normalize(r'''
            discograph.models.ArtistCredit(
                artist=discograph.models.Artist(
                    discogs_id=1,
                    has_been_scraped=False,
                    name='Persuader, The',
                    ),
                discogs_id=1,
                name='Persuader, The',
                )
            ''')

    def test_2(self):
        source = '''
            <extraartists>
                <artist>
                    <id>239</id>
                    <name>Jesper Dahlb\xe4ck</name>
                    <anv/>
                    <join/>
                    <role>Music By [All Tracks By]</role>
                    <tracks/>
                </artist>
            </extraartists>
            '''
        element = ElementTree.fromstring(source)
        artist_credits = models.ArtistCredit.from_elements(element)
        assert format(artist_credits[0]) == stringtools.normalize(r'''
            discograph.models.ArtistCredit(
                artist=discograph.models.Artist(
                    discogs_id=239,
                    has_been_scraped=False,
                    name='Jesper Dahlbäck',
                    ),
                discogs_id=239,
                name='Jesper Dahlbäck',
                roles=[
                    discograph.models.ArtistRole(
                        detail='All Tracks By',
                        name='Music By',
                        ),
                    ],
                )
            ''')