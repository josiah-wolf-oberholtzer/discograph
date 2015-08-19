# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from discograph import bootstrap
from discograph import models


class Test(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('discograph:test')

    def test_01(self):
        iterator = bootstrap.get_iterator('artist')
        artist_element = next(iterator)
        assert bootstrap.prettify(artist_element) == bootstrap.normalize(u'''
            <?xml version="1.0" ?>
            <artist>
                <id>1</id>
                <name>Persuader, The</name>
                <realname>Jesper Dahlbäck</realname>
                <profile/>
                <data_quality>Correct</data_quality>
                <namevariations>
                    <name>Persuader</name>
                    <name>Presuader, The</name>
                </namevariations>
                <aliases>
                    <name>Dick Track</name>
                    <name>Faxid</name>
                    <name>Groove Machine</name>
                    <name>Janne Me' Amazonen</name>
                    <name>Jesper Dahlbäck</name>
                    <name>Lenk</name>
                    <name>Pinguin Man, The</name>
                </aliases>
            </artist>
            ''')
        artist_document = models.Artist.from_element(artist_element)