from discograph import models
import unittest
import xml.etree.cElementTree


class Test(unittest.TestCase):

    def test_1(self):
        element = xml.etree.cElementTree.fromstring('<test></test>')
        element.text = (
            'Shekere [Xequere, Original Musician], Guiro [Original Musician], '
            'Claves [Original Musician]'
            )
        roles = models.ArtistRole.from_element(element)
        assert roles == [
            models.ArtistRole(
                name='Shekere',
                detail='Xequere, Original Musician',
                ),
            models.ArtistRole(name='Guiro', detail='Original Musician'),
            models.ArtistRole(name='Claves', detail='Original Musician'),
            ]

    def test_2(self):
        element = xml.etree.cElementTree.fromstring('<test></test>')
        element.text = (
            'Co-producer, Arranged By, Directed By, Other [Guided By], '
            'Other [Created By]'
            )
        roles = models.ArtistRole.from_element(element)
        assert roles == [
            models.ArtistRole(name='Co-producer'),
            models.ArtistRole(name='Arranged By'),
            models.ArtistRole(name='Directed By'),
            models.ArtistRole(name='Other', detail='Guided By'),
            models.ArtistRole(name='Other', detail='Created By'),
            ]

    def test_3(self):
        element = xml.etree.cElementTree.fromstring('<test></test>')
        element.text = (
            'Organ [Original Musician], '
            'Electric Piano [Rhodes, Original Musician]'
            )
        roles = models.ArtistRole.from_element(element)
        assert roles == [
            models.ArtistRole(
                name='Organ',
                detail='Original Musician',
                ),
            models.ArtistRole(
                name='Electric Piano',
                detail='Rhodes, Original Musician',
                ),
            ]

    def test_4(self):
        element = xml.etree.cElementTree.fromstring('<test></test>')
        element.text = "Photography By ['hats' And 'spray' Photos By]"
        roles = models.ArtistRole.from_element(element)
        assert roles == [
            models.ArtistRole(
                name='Photography By',
                detail="'hats' And 'spray' Photos By",
                ),
            ]

    def test_5(self):
        element = xml.etree.cElementTree.fromstring('<test></test>')
        element.text = 'Strings '
        roles = models.ArtistRole.from_element(element)
        assert roles == [
            models.ArtistRole(name='Strings'),
            ]

    def test_6(self):
        element = xml.etree.cElementTree.fromstring('<test></test>')
        element.text = 'Piano, Synthesizer [Moog], Programmed By'
        roles = models.ArtistRole.from_element(element)
        assert roles == [
            models.ArtistRole(name='Piano'),
            models.ArtistRole(name='Synthesizer', detail='Moog'),
            models.ArtistRole(name='Programmed By'),
            ]

    def test_7(self):
        element = xml.etree.cElementTree.fromstring('<test></test>')
        element.text = 'Percussion [Misc.]'
        roles = models.ArtistRole.from_element(element)
        assert roles == [
            models.ArtistRole(name='Percussion', detail='Misc.'),
            ]

    def test_8(self):
        element = xml.etree.cElementTree.fromstring('<test></test>')
        element.text = 'Painting [Uncredited; Detail Of <i>"The Transfiguration"</i>]'
        roles = models.ArtistRole.from_element(element)
        assert roles == [
            models.ArtistRole(
                name='Painting',
                detail='Uncredited; Detail Of <i>"The Transfiguration"</i>',
                ),
            ]

    def test_9(self):
        element = xml.etree.cElementTree.fromstring('<test></test>')
        element.text = 'Composed By, Words By [elemented By], Producer'
        roles = models.ArtistRole.from_element(element)
        assert roles == [
            models.ArtistRole(name='Composed By'),
            models.ArtistRole(name='Words By', detail='elemented By'),
            models.ArtistRole(name='Producer'),
            ]

    def test_10(self):
        element = xml.etree.cElementTree.fromstring('<test></test>')
        element.text = 'Engineer [Remix] [Assistant], Producer'
        roles = models.ArtistRole.from_element(element)
        assert roles == [
            models.ArtistRole(name='Engineer', detail='Remix, Assistant'),
            models.ArtistRole(name='Producer'),
            ]

    def test_11(self):
        element = xml.etree.cElementTree.fromstring('<test></test>')
        element.text = 'Performer [Enigmatic [K] Voice, Moog, Korg Vocoder], Lyrics By'
        roles = models.ArtistRole.from_element(element)
        assert roles == [
            models.ArtistRole(name='Performer', detail='Enigmatic [K] Voice, Moog, Korg Vocoder'),
            models.ArtistRole(name='Lyrics By'),
            ]