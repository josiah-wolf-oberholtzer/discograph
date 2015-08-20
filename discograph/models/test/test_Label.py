# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from abjad import stringtools
from discograph import bootstrap
from discograph import models


class Test(unittest.TestCase):

    def setUp(self):
        database_name = 'discograph:test'
        client = mongoengine.connect(database_name)
        client.drop_database(database_name)

    def test_01(self):
        iterator = bootstrap.get_iterator('label')
        label_element = next(iterator)
        label_element = next(iterator)
        label_element = next(iterator)
        actual = stringtools.normalize(bootstrap.prettify(label_element))
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
        label_document = models.Label.from_element(label_element)
        actual = format(label_document)
        expected = stringtools.normalize(u'''
            discograph.models.Label(
                discogs_id=3,
                has_been_scraped=True,
                name=u'Seasons Recordings',
                sublabels=[
                    discograph.models.Label(
                        has_been_scraped=False,
                        name=u'Seasons Classics',
                        sublabels=[],
                        ),
                    discograph.models.Label(
                        has_been_scraped=False,
                        name=u'Seasons Limited',
                        sublabels=[],
                        ),
                    ],
                )
            ''')
        assert actual == expected