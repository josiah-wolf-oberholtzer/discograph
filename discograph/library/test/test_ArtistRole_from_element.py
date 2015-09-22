from discograph import library
import unittest
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree


class Test(unittest.TestCase):

    def test_1(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = (
            'Shekere [Xequere, Original Musician], Guiro [Original Musician], '
            'Claves [Original Musician]'
            )
        roles = library.ArtistRole.from_element(element)
        assert roles == [
            library.ArtistRole(
                name='Shekere',
                detail='Xequere, Original Musician',
                ),
            library.ArtistRole(name='Guiro', detail='Original Musician'),
            library.ArtistRole(name='Claves', detail='Original Musician'),
            ]

    def test_2(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = (
            'Co-producer, Arranged By, Directed By, Other [Guided By], '
            'Other [Created By]'
            )
        roles = library.ArtistRole.from_element(element)
        assert roles == [
            library.ArtistRole(name='Co-producer'),
            library.ArtistRole(name='Arranged By'),
            library.ArtistRole(name='Directed By'),
            library.ArtistRole(name='Other', detail='Guided By'),
            library.ArtistRole(name='Other', detail='Created By'),
            ]

    def test_3(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = (
            'Organ [Original Musician], '
            'Electric Piano [Rhodes, Original Musician]'
            )
        roles = library.ArtistRole.from_element(element)
        assert roles == [
            library.ArtistRole(
                name='Organ',
                detail='Original Musician',
                ),
            library.ArtistRole(
                name='Electric Piano',
                detail='Rhodes, Original Musician',
                ),
            ]

    def test_4(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = "Photography By ['hats' And 'spray' Photos By]"
        roles = library.ArtistRole.from_element(element)
        assert roles == [
            library.ArtistRole(
                name='Photography By',
                detail="'hats' And 'spray' Photos By",
                ),
            ]

    def test_5(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Strings '
        roles = library.ArtistRole.from_element(element)
        assert roles == [
            library.ArtistRole(name='Strings'),
            ]

    def test_6(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Piano, Synthesizer [Moog], Programmed By'
        roles = library.ArtistRole.from_element(element)
        assert roles == [
            library.ArtistRole(name='Piano'),
            library.ArtistRole(name='Synthesizer', detail='Moog'),
            library.ArtistRole(name='Programmed By'),
            ]

    def test_7(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Percussion [Misc.]'
        roles = library.ArtistRole.from_element(element)
        assert roles == [
            library.ArtistRole(name='Percussion', detail='Misc.'),
            ]

    def test_8(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Painting [Uncredited; Detail Of <i>"The Transfiguration"</i>]'
        roles = library.ArtistRole.from_element(element)
        assert roles == [
            library.ArtistRole(
                name='Painting',
                detail='Uncredited; Detail Of <i>"The Transfiguration"</i>',
                ),
            ]

    def test_9(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Composed By, Words By [elemented By], Producer'
        roles = library.ArtistRole.from_element(element)
        assert roles == [
            library.ArtistRole(name='Composed By'),
            library.ArtistRole(name='Words By', detail='elemented By'),
            library.ArtistRole(name='Producer'),
            ]

    def test_10(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Engineer [Remix] [Assistant], Producer'
        roles = library.ArtistRole.from_element(element)
        assert roles == [
            library.ArtistRole(name='Engineer', detail='Remix, Assistant'),
            library.ArtistRole(name='Producer'),
            ]

    def test_11(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Performer [Enigmatic [K] Voice, Moog, Korg Vocoder], Lyrics By'
        roles = library.ArtistRole.from_element(element)
        assert roles == [
            library.ArtistRole(name='Performer', detail='Enigmatic [K] Voice, Moog, Korg Vocoder'),
            library.ArtistRole(name='Lyrics By'),
            ]