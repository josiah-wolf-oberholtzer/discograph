import discograph
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
        roles = discograph.CreditRole.from_element(element)
        assert roles == [
            discograph.CreditRole(
                name='Shekere',
                detail='Xequere, Original Musician',
                ),
            discograph.CreditRole(name='Guiro', detail='Original Musician'),
            discograph.CreditRole(name='Claves', detail='Original Musician'),
            ]

    def test_2(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = (
            'Co-producer, Arranged By, Directed By, Other [Guided By], '
            'Other [Created By]'
            )
        roles = discograph.CreditRole.from_element(element)
        assert roles == [
            discograph.CreditRole(name='Co-producer'),
            discograph.CreditRole(name='Arranged By'),
            discograph.CreditRole(name='Directed By'),
            discograph.CreditRole(name='Other', detail='Guided By'),
            discograph.CreditRole(name='Other', detail='Created By'),
            ]

    def test_3(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = (
            'Organ [Original Musician], '
            'Electric Piano [Rhodes, Original Musician]'
            )
        roles = discograph.CreditRole.from_element(element)
        assert roles == [
            discograph.CreditRole(
                name='Organ',
                detail='Original Musician',
                ),
            discograph.CreditRole(
                name='Electric Piano',
                detail='Rhodes, Original Musician',
                ),
            ]

    def test_4(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = "Photography By ['hats' And 'spray' Photos By]"
        roles = discograph.CreditRole.from_element(element)
        assert roles == [
            discograph.CreditRole(
                name='Photography By',
                detail="'hats' And 'spray' Photos By",
                ),
            ]

    def test_5(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Strings '
        roles = discograph.CreditRole.from_element(element)
        assert roles == [
            discograph.CreditRole(name='Strings'),
            ]

    def test_6(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Piano, Synthesizer [Moog], Programmed By'
        roles = discograph.CreditRole.from_element(element)
        assert roles == [
            discograph.CreditRole(name='Piano'),
            discograph.CreditRole(name='Synthesizer', detail='Moog'),
            discograph.CreditRole(name='Programmed By'),
            ]

    def test_7(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Percussion [Misc.]'
        roles = discograph.CreditRole.from_element(element)
        assert roles == [
            discograph.CreditRole(name='Percussion', detail='Misc.'),
            ]

    def test_8(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Painting [Uncredited; Detail Of <i>"The Transfiguration"</i>]'
        roles = discograph.CreditRole.from_element(element)
        assert roles == [
            discograph.CreditRole(
                name='Painting',
                detail='Uncredited; Detail Of <i>"The Transfiguration"</i>',
                ),
            ]

    def test_9(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Composed By, Words By [elemented By], Producer'
        roles = discograph.CreditRole.from_element(element)
        assert roles == [
            discograph.CreditRole(name='Composed By'),
            discograph.CreditRole(name='Words By', detail='elemented By'),
            discograph.CreditRole(name='Producer'),
            ]

    def test_10(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Engineer [Remix] [Assistant], Producer'
        roles = discograph.CreditRole.from_element(element)
        assert roles == [
            discograph.CreditRole(name='Engineer', detail='Remix, Assistant'),
            discograph.CreditRole(name='Producer'),
            ]

    def test_11(self):
        element = ElementTree.fromstring('<test></test>')
        element.text = 'Performer [Enigmatic [K] Voice, Moog, Korg Vocoder], Lyrics By'
        roles = discograph.CreditRole.from_element(element)
        assert roles == [
            discograph.CreditRole(name='Performer', detail='Enigmatic [K] Voice, Moog, Korg Vocoder'),
            discograph.CreditRole(name='Lyrics By'),
            ]