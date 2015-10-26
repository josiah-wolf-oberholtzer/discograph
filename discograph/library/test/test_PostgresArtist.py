# -*- encoding: utf-8 -*-
import discograph
import unittest
from abjad import stringtools
from discograph.library.Bootstrapper import Bootstrapper


class Test(unittest.TestCase):

    def test_01(self):
        iterator = Bootstrapper.get_iterator('artist')
        element = next(iterator)
        artist = discograph.PostgresArtist.from_element(element)
        actual = format(artist)
        expected = stringtools.normalize(u"""
            discograph.library.postgres.PostgresArtist(
                aliases={
                    'Dick Track': None,
                    'Faxid': None,
                    'Groove Machine': None,
                    "Janne Me' Amazonen": None,
                    'Jesper Dahlbäck': None,
                    'Lenk': None,
                    'The Pinguin Man': None,
                    },
                id=1,
                name='The Persuader',
                name_variations=['Persuader', 'The Presuader'],
                real_name='Jesper Dahlbäck',
                )
            """)
        assert actual == expected