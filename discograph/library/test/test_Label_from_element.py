# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from abjad import stringtools
from discograph.library.Bootstrapper import Bootstrapper
from discograph import library


class Test(unittest.TestCase):

    database_name = 'discograph:test'

    def setUp(self):
        self.database = mongoengine.connect(self.database_name)

    def tearDown(self):
        self.database.drop_database(self.database_name)
        self.database.close()

    def test_01(self):
        iterator = Bootstrapper.get_iterator('label')
        label_element = next(iterator)
        label_element = next(iterator)
        label_element = next(iterator)
        actual = stringtools.normalize(Bootstrapper.prettify(label_element))
        expected = stringtools.normalize(u'''
            <?xml version="1.0" ?>
            <label>
                <id>3</id>
                <name>Seasons Recordings</name>
                <contactinfo>Seasons Recordings
            2236 Pacific Avenue
            Suite D
            Costa Mesa, CA 92627

            Jamie Thinnes

            Tel: 949-574-5255
            Fax: 949-574-0255

            jthinnes@seasonsrecordings.com
            info@seasonsrecordings.com
            </contactinfo>
                <profile>California Deep-House Label Founded By Jamie Thinnes.
            The First 10 Records Were Released on [l=Earthtones Recordings]
            </profile>
                <data_quality>Correct</data_quality>
                <sublabels>
                    <label>Seasons Classics</label>
                    <label>Seasons Limited</label>
                </sublabels>
            </label>
            ''')
        assert actual.splitlines() == expected.splitlines()
        label_document = library.Label.from_element(label_element)
        actual = format(label_document)
        expected = stringtools.normalize(u'''
            discograph.library.Label(
                discogs_id=3,
                name='Seasons Recordings',
                sublabels=[
                    discograph.library.LabelReference(
                        name='Seasons Classics',
                        ),
                    discograph.library.LabelReference(
                        name='Seasons Limited',
                        ),
                    ],
                )
            ''')
        assert actual == expected