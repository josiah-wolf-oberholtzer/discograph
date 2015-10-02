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
        roles = library.CreditRole.from_element(element)
        assert roles == [
            library.CreditRole(
                name='Shekere',
                detail='Xequere, Original Musician',
                ),
            library.CreditRole(name='Guiro', detail='Original Musician'),
            library.CreditRole(name='Claves', detail='Original Musician'),
            ]

    def test_2(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = (
            'Co-producer, Arranged By, Directed By, Other [Guided By], '
            'Other [Created By]'
            )
        roles = library.CreditRole.from_element(element)
        assert roles == [
            library.CreditRole(name='Co-producer'),
            library.CreditRole(name='Arranged By'),
            library.CreditRole(name='Directed By'),
            library.CreditRole(name='Other', detail='Guided By'),
            library.CreditRole(name='Other', detail='Created By'),
            ]

    def test_3(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = (
            'Organ [Original Musician], '
            'Electric Piano [Rhodes, Original Musician]'
            )
        roles = library.CreditRole.from_element(element)
        assert roles == [
            library.CreditRole(
                name='Organ',
                detail='Original Musician',
                ),
            library.CreditRole(
                name='Electric Piano',
                detail='Rhodes, Original Musician',
                ),
            ]

    def test_4(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = "Photography By ['hats' And 'spray' Photos By]"
        roles = library.CreditRole.from_element(element)
        assert roles == [
            library.CreditRole(
                name='Photography By',
                detail="'hats' And 'spray' Photos By",
                ),
            ]

    def test_5(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Strings '
        roles = library.CreditRole.from_element(element)
        assert roles == [
            library.CreditRole(name='Strings'),
            ]

    def test_6(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Piano, Synthesizer [Moog], Programmed By'
        roles = library.CreditRole.from_element(element)
        assert roles == [
            library.CreditRole(name='Piano'),
            library.CreditRole(name='Synthesizer', detail='Moog'),
            library.CreditRole(name='Programmed By'),
            ]

    def test_7(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Percussion [Misc.]'
        roles = library.CreditRole.from_element(element)
        assert roles == [
            library.CreditRole(name='Percussion', detail='Misc.'),
            ]

    def test_8(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Painting [Uncredited; Detail Of <i>"The Transfiguration"</i>]'
        roles = library.CreditRole.from_element(element)
        assert roles == [
            library.CreditRole(
                name='Painting',
                detail='Uncredited; Detail Of <i>"The Transfiguration"</i>',
                ),
            ]

    def test_9(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Composed By, Words By [elemented By], Producer'
        roles = library.CreditRole.from_element(element)
        assert roles == [
            library.CreditRole(name='Composed By'),
            library.CreditRole(name='Words By', detail='elemented By'),
            library.CreditRole(name='Producer'),
            ]

    def test_10(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Engineer [Remix] [Assistant], Producer'
        roles = library.CreditRole.from_element(element)
        assert roles == [
            library.CreditRole(name='Engineer', detail='Remix, Assistant'),
            library.CreditRole(name='Producer'),
            ]

    def test_11(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Performer [Enigmatic [K] Voice, Moog, Korg Vocoder], Lyrics By'
        roles = library.CreditRole.from_element(element)
        assert roles == [
            library.CreditRole(name='Performer', detail='Enigmatic [K] Voice, Moog, Korg Vocoder'),
            library.CreditRole(name='Lyrics By'),
            ]