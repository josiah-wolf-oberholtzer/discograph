# -*- encoding: utf-8 -*-
import discograph
import unittest
from abjad import stringtools
from discograph.library.Bootstrapper import Bootstrapper


class Test(unittest.TestCase):

    def test_01(self):
        iterator = Bootstrapper.get_iterator('label')
        element = next(iterator)
        label = discograph.PostgresLabel.from_element(element)
        actual = stringtools.normalize(format(label))
        expected = stringtools.normalize(r'''
            discograph.library.PostgresLabel(
                id=1,
                name='Planet E',
                profile='Classic Techno label from Detroit, USA.\r\n[b]Label owner:[/b] [a=Carl Craig].\r\n',
                sublabels={
                    'Antidote (4)': None,
                    'Community Projects': None,
                    'Guilty Pleasures': None,
                    'I Ner Zon Sounds': None,
                    'Planet E Communications, Inc.': None,
                    'TWPENTY': None,
                    },
                urls=[
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
                )
            ''')
        assert actual == expected