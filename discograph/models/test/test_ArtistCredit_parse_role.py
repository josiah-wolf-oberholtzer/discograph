from discograph import models
import unittest


class Test(unittest.TestCase):

    def test_1(self):
        text = (
            'Shekere [Xequere, Original Musician], Guiro [Original Musician], '
            'Claves [Original Musician]'
            )
        roles = models.ArtistCredit.parse_roles(text)
        assert roles == [
            'Shekere [Xequere, Original Musician]',
            'Guiro [Original Musician]',
            'Claves [Original Musician]',
            ]

    def test_2(self):
        text = (
            'Co-producer, Arranged By, Directed By, Other [Guided By], '
            'Other [Created By]'
            )
        roles = models.ArtistCredit.parse_roles(text)
        assert roles == [
            'Co-producer',
            'Arranged By',
            'Directed By',
            'Other [Guided By]',
            'Other [Created By]',
            ]

    def test_3(self):
        text = (
            'Organ [Original Musician], '
            'Electric Piano [Rhodes, Original Musician]'
            )
        roles = models.ArtistCredit.parse_roles(text)
        assert roles == [
            'Organ [Original Musician]',
            'Electric Piano [Rhodes, Original Musician]',
            ]

    def test_4(self):
        text = "Photography By ['hats' And 'spray' Photos By]"
        roles = models.ArtistCredit.parse_roles(text)
        assert roles == [
            "Photography By ['hats' And 'spray' Photos By]"
            ]

    def test_5(self):
        text = 'Strings '
        roles = models.ArtistCredit.parse_roles(text)
        assert roles == [
            'Strings',
            ]

    def test_6(self):
        text = 'Piano, Synthesizer [Moog], Programmed By'
        roles = models.ArtistCredit.parse_roles(text)
        assert roles == [
            'Piano',
            'Synthesizer [Moog]',
            'Programmed By',
            ]

    def test_7(self):
        text = 'Percussion [Misc.]'
        roles = models.ArtistCredit.parse_roles(text)
        assert roles == [
            'Percussion [Misc.]'
            ]

    def test_8(self):
        text = 'Painting [Uncredited; Detail Of <i>"The Transfiguration"</i>]'
        roles = models.ArtistCredit.parse_roles(text)
        assert roles == [
            'Painting [Uncredited; Detail Of <i>"The Transfiguration"</i>]'
            ]

    def test_9(self):
        text = 'Composed By, Words By [Texted By], Producer'
        roles = models.ArtistCredit.parse_roles(text)
        assert roles == [
            'Composed By',
            'Words By [Texted By]',
            'Producer',
            ]