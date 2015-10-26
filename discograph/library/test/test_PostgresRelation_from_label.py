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
        source = stringtools.normalize('''
            <?xml version="1.0" ?>
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
        label_document = discograph.PostgresLabel.from_element(label_element)
        label_document.sublabels['Seasons Classics'] = 297127
        label_document.sublabels['Seasons Limited'] = 66542
        actual = discograph.PostgresRelation.from_label(label_document)
        expected = [
            {
                'entity_one_id': 66542,
                'entity_one_type': discograph.PostgresRelation.EntityType.LABEL,
                'entity_two_id': 3,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'role': 'Sublabel Of',
                },
            {
                'entity_one_id': 297127,
                'entity_one_type': discograph.PostgresRelation.EntityType.LABEL,
                'entity_two_id': 3,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'role': 'Sublabel Of',
                },
            ]
        assert actual == expected