# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from abjad.tools import stringtools
from discograph import bootstrap
from discograph import models
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
        iterator = bootstrap.Bootstrap.get_iterator('release')
        release_element = next(iterator)
        release_document = models.Release.from_element(release_element)
        relations = models.Relation.from_release(release_document)
        actual = '\n'.join(format(_) for _ in relations)
        expected = stringtools.normalize(r'''
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=1,
                entity_one_name='Persuader, The',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_name='Svek',
                entity_two_type=discograph.models.Relation.EntityType.LABEL,
                release_id=1,
                role_name='Released On',
                year=1999,
                )
            ''')
        assert actual == expected

    def test_02(self):
        source = stringtools.normalize('''
        <?xml version="1.0" ?>
        <release id="103" status="Accepted">
            <artists>
                <artist>
                    <id>194</id>
                    <name>Various</name>
                    <anv/>
                    <join/>
                    <role/>
                    <tracks/>
                </artist>
            </artists>
            <title>The Necessary EP</title>
            <labels>
                <label catno="NT006" name="Nordic Trax"/>
            </labels>
            <extraartists/>
            <formats>
                <format name="Vinyl" qty="1" text="">
                    <descriptions>
                        <description>12&quot;</description>
                        <description>EP</description>
                    </descriptions>
                </format>
            </formats>
            <genres>
                <genre>Electronic</genre>
            </genres>
            <styles>
                <style>Deep House</style>
            </styles>
            <country>Canada</country>
            <released>1999-00-00</released>
            <data_quality>Correct</data_quality>
            <tracklist>
                <track>
                    <position>A1</position>
                    <title>K2morrow</title>
                    <duration/>
                    <artists>
                        <artist>
                            <id>195</id>
                            <name>Peter Hecher</name>
                            <anv/>
                            <join/>
                            <role/>
                            <tracks/>
                        </artist>
                    </artists>
                </track>
                <track>
                    <position>A2</position>
                    <title>The Disco Man</title>
                    <duration/>
                    <artists>
                        <artist>
                            <id>195</id>
                            <name>Peter Hecher</name>
                            <anv/>
                            <join/>
                            <role/>
                            <tracks/>
                        </artist>
                    </artists>
                </track>
                <track>
                    <position>B1</position>
                    <title>Making Changes (4am Vibez)</title>
                    <duration/>
                    <artists>
                        <artist>
                            <id>196</id>
                            <name>Aaronz</name>
                            <anv/>
                            <join/>
                            <role/>
                            <tracks/>
                        </artist>
                    </artists>
                </track>
                <track>
                    <position>B2</position>
                    <title>Up Jumped The Boogie</title>
                    <duration/>
                    <artists>
                        <artist>
                            <id>197</id>
                            <name>Sea To Sky</name>
                            <anv/>
                            <join/>
                            <role/>
                            <tracks/>
                        </artist>
                    </artists>
                </track>
            </tracklist>
            <videos>
                <video duration="395" embed="true" src="http://www.youtube.com/watch?v=CmFYUEcD0Xs">
                    <title>K2morrow [Original Mix] - Peter Hecher</title>
                    <description>K2morrow [Original Mix] - Peter Hecher</description>
                </video>
            </videos>
            <companies/>
        </release>
        ''')
        release_element = ElementTree.fromstring(source)
        release_document = models.Release.from_element(release_element)
        relations = models.Relation.from_release(release_document)
        actual = '\n'.join(format(_) for _ in relations)
        expected = stringtools.normalize(r'''
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=195,
                entity_one_name='Peter Hecher',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_name='Nordic Trax',
                entity_two_type=discograph.models.Relation.EntityType.LABEL,
                release_id=103,
                role_name='Released On',
                year=1999,
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=196,
                entity_one_name='Aaronz',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_name='Nordic Trax',
                entity_two_type=discograph.models.Relation.EntityType.LABEL,
                release_id=103,
                role_name='Released On',
                year=1999,
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=197,
                entity_one_name='Sea To Sky',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_name='Nordic Trax',
                entity_two_type=discograph.models.Relation.EntityType.LABEL,
                release_id=103,
                role_name='Released On',
                year=1999,
                )
            ''')
        assert actual == expected