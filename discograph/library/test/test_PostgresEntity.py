# -*- encoding: utf-8 -*-
from abjad import stringtools
import discograph
import unittest


class Test(unittest.TestCase):

    def test_01(self):
        iterator = discograph.Bootstrapper.get_iterator('artist')
        element = next(iterator)
        entity = discograph.PostgresEntity.from_element(element)
        actual = stringtools.normalize(format(entity))
        expected = stringtools.normalize(u"""
            discograph.library.postgres.PostgresEntity(
                entities={
                    'aliases': {
                        'Dick Track': None,
                        'Faxid': None,
                        'Groove Machine': None,
                        "Janne Me' Amazonen": None,
                        'Jesper Dahlbäck': None,
                        'Lenk': None,
                        'The Pinguin Man': None,
                        },
                    },
                entity_id=1,
                entity_type=1,
                metadata={
                    'name_variations': ['Persuader', 'The Presuader'],
                    'profile': None,
                    'real_name': 'Jesper Dahlbäck',
                    },
                name='The Persuader',
                )
            """)
        assert actual == expected

    def test_02(self):
        iterator = discograph.Bootstrapper.get_iterator('label')
        element = next(iterator)
        entity = discograph.PostgresEntity.from_element(element)
        actual = stringtools.normalize(format(entity))
        expected = stringtools.normalize(r'''
            discograph.library.postgres.PostgresEntity(
                entities={
                    'sublabels': {
                        'Antidote (4)': None,
                        'Community Projects': None,
                        'Guilty Pleasures': None,
                        'I Ner Zon Sounds': None,
                        'Planet E Communications, Inc.': None,
                        'TWPENTY': None,
                        },
                    },
                entity_id=1,
                entity_type=2,
                metadata={
                    'profile': 'Classic Techno label from Detroit, USA.\n[b]Label owner:[/b] [a=Carl Craig].\n',
                    'urls': [
                        'http://planet-e.net',
                        'http://planetecommunications.bandcamp.com',
                        'http://www.discogs.com/user/planetedetroit',
                        'http://www.facebook.com/planetedetroit',
                        'http://www.flickr.com/photos/planetedetroit',
                        'http://plus.google.com/100841702106447505236',
                        'http://myspace.com/planetecom',
                        'http://myspace.com/planetedetroit',
                        'http://soundcloud.com/planetedetroit',
                        'http://twitter.com/planetedetroit',
                        'http://vimeo.com/user1265384',
                        'http://www.youtube.com/user/planetedetroit',
                        'http://en.wikipedia.org/wiki/Planet_E_Communications',
                        ],
                    },
                name='Planet E',
                )
            ''')
        assert actual == expected