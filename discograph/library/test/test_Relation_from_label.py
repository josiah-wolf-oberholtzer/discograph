# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from abjad.tools import stringtools
from discograph import library
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

    def test_01(self):

        source = stringtools.normalize('''
            <label>
                <id>3</id>
                <name>Seasons Recordings</name>
                <sublabels>
                    <label>Seasons Classics</label>
                    <label>Seasons Limited</label>
                </sublabels>
            </label>
            ''')
        label_element = ElementTree.fromstring(source)
        label_document = library.Label.from_element(label_element)
        label_document.save()

        source = stringtools.normalize('''
            <label>
                <id>297127</id>
                <name>Seasons Classics</name>
                <parentLabel>Seasons Recordings</parentLabel>
            </label>
            ''')
        sublabel_element = ElementTree.fromstring(source)
        sublabel_document = library.Label.from_element(sublabel_element)
        sublabel_document.save()

        source = stringtools.normalize('''
            <label>
                <id>66542</id>
                <name>Seasons Limited</name>
                <parentLabel>Seasons Recordings</parentLabel>
            </label>
            ''')
        sublabel_element = ElementTree.fromstring(source)
        sublabel_document = library.Label.from_element(sublabel_element)
        sublabel_document.save()

        label_document.resolve_references()
        label_document.save()
        label_document.reload()
        sublabels = label_document.sublabels
        assert len(sublabels) == 2
        assert sorted(_.discogs_id for _ in sublabels) == [66542, 297127]

        relations = library.Relation.from_label(label_document)
        actual = '\n'.join(format(_) for _ in relations)
        expected = stringtools.normalize(r'''
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.RELATION,
                entity_one_id=66542,
                entity_one_name='Seasons Limited',
                entity_one_type=discograph.library.Relation.EntityType.LABEL,
                entity_two_id=3,
                entity_two_name='Seasons Recordings',
                entity_two_type=discograph.library.Relation.EntityType.LABEL,
                role_name='Sublabel Of',
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.RELATION,
                entity_one_id=297127,
                entity_one_name='Seasons Classics',
                entity_one_type=discograph.library.Relation.EntityType.LABEL,
                entity_two_id=3,
                entity_two_name='Seasons Recordings',
                entity_two_type=discograph.library.Relation.EntityType.LABEL,
                role_name='Sublabel Of',
                )
            ''')
        assert actual == expected