# -*- encoding: utf-8 -*-
import discograph
import unittest
from abjad.tools import stringtools
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree


class Test(unittest.TestCase):

    def test_01(self):
        source = stringtools.normalize(r'''
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
        artist_element = ElementTree.fromstring(source)
        artist_document = discograph.PostgresArtist.from_element(artist_element)
        for i, alias_name in enumerate(sorted(artist_document.aliases.keys()), 100000000):
            artist_document.aliases[alias_name] = i
        for i, member_name in enumerate(sorted(artist_document.members.keys()), 200000000):
            artist_document.members[member_name] = i
        actual = discograph.PostgresRelation.from_artist(artist_document)
        expected = [
            {
                'entity_one': discograph.PostgresArtist(id=2),
                'entity_two': discograph.PostgresArtist(id=100000000),
                'role': 'Alias',
                },
            {
                'entity_one': discograph.PostgresArtist(id=2),
                'entity_two': discograph.PostgresArtist(id=100000001),
                'role': 'Alias',
                },
            {
                'entity_one': discograph.PostgresArtist(id=2),
                'entity_two': discograph.PostgresArtist(id=100000002),
                'role': 'Alias',
                },
            {
                'entity_one': discograph.PostgresArtist(id=2),
                'entity_two': discograph.PostgresArtist(id=100000003),
                'role': 'Alias',
                },
            {
                'entity_one': discograph.PostgresArtist(id=2),
                'entity_two': discograph.PostgresArtist(id=100000004),
                'role': 'Alias',
                },
            {
                'entity_one': discograph.PostgresArtist(id=200000000),
                'entity_two': discograph.PostgresArtist(id=2),
                'role': 'Member Of',
                },
            {
                'entity_one': discograph.PostgresArtist(id=200000001),
                'entity_two': discograph.PostgresArtist(id=2),
                'role': 'Member Of',
                },
            ]
        assert actual == expected