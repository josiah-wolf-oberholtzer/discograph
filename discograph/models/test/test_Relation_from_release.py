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
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.WRITING_AND_ARRANGEMENT,
                entity_one_id=239,
                entity_one_name='Jesper Dahlbäck',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_id=1,
                entity_two_name='Persuader, The',
                entity_two_type=discograph.models.Relation.EntityType.ARTIST,
                release_id=1,
                role_name='Music By',
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

    def test_03(self):
        source = stringtools.normalize('''
            <?xml version="1.0" ?>
            <release id="5" status="Accepted">
                <artists>
                    <artist>
                        <id>22</id>
                        <name>Datacide</name>
                        <anv/>
                        <join>,</join>
                        <role/>
                        <tracks/>
                    </artist>
                </artists>
                <title>Flowerhead</title>
                <labels>
                    <label catno="RI 026" name="Rather Interesting"/>
                    <label catno="RI026" name="Rather Interesting"/>
                </labels>
                <extraartists>
                    <artist>
                        <id>539207</id>
                        <name>Linger Decoree</name>
                        <anv/>
                        <join/>
                        <role>Cover, Design [Logo Designs]</role>
                        <tracks/>
                    </artist>
                    <artist>
                        <id>25</id>
                        <name>Tetsu Inoue</name>
                        <anv/>
                        <join/>
                        <role>Performer [Datacide Are]</role>
                        <tracks/>
                    </artist>
                    <artist>
                        <id>519207</id>
                        <name>Uwe Schmidt</name>
                        <anv/>
                        <join/>
                        <role>Performer [Datacide Are]</role>
                        <tracks/>
                    </artist>
                    <artist>
                        <id>22</id>
                        <name>Datacide</name>
                        <anv/>
                        <join/>
                        <role>Producer</role>
                        <tracks/>
                    </artist>
                </extraartists>
                <formats>
                    <format name="CD" qty="1" text="">
                        <descriptions>
                            <description>Album</description>
                            <description>Limited Edition</description>
                        </descriptions>
                    </format>
                </formats>
                <genres>
                    <genre>Electronic</genre>
                </genres>
                <styles>
                    <style>Abstract</style>
                    <style>Ambient</style>
                </styles>
                <country>Germany</country>
                <released>1995</released>
                <tracklist>
                    <track>
                        <position>1</position>
                        <title>Flashback Signal</title>
                        <duration>15:54</duration>
                        <extraartists>
                            <artist>
                                <id>415403</id>
                                <name>Ingrid Baier</name>
                                <anv>Ingrid</anv>
                                <join/>
                                <role>Voice</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>2</position>
                        <title>Flowerhead</title>
                        <duration>9:33</duration>
                    </track>
                    <track>
                        <position>3</position>
                        <title>Deep Chair</title>
                        <duration>14:05</duration>
                    </track>
                    <track>
                        <position>4</position>
                        <title>So Much Light</title>
                        <duration>12:02</duration>
                    </track>
                    <track>
                        <position>5</position>
                        <title>Sixties Out Of Tune</title>
                        <duration>13:05</duration>
                    </track>
                </tracklist>
                <companies>
                    <company>
                        <id>403521</id>
                        <name>Del Haze Entertainment</name>
                        <catno/>
                        <entity_type>8</entity_type>
                        <entity_type_name>Marketed By</entity_type_name>
                        <resource_url>http://api.discogs.com/labels/403521</resource_url>
                    </company>
                    <company>
                        <id>291931</id>
                        <name>CD Plant MFG</name>
                        <catno/>
                        <entity_type>10</entity_type>
                        <entity_type_name>Manufactured By</entity_type_name>
                        <resource_url>http://api.discogs.com/labels/291931</resource_url>
                    </company>
                    <company>
                        <id>265233</id>
                        <name>Sel i/s/c</name>
                        <catno/>
                        <entity_type>26</entity_type>
                        <entity_type_name>Produced At</entity_type_name>
                        <resource_url>http://api.discogs.com/labels/265233</resource_url>
                    </company>
                </companies>
            </release>
            ''')
        release_element = ElementTree.fromstring(source)
        release_document = models.Release.from_element(release_element)
        relations = models.Relation.from_release(release_document)
        actual = '\n'.join(format(_) for _ in relations)
        expected = stringtools.normalize(r'''
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.RELATION,
                entity_one_id=22,
                entity_one_name='Datacide',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_name='Rather Interesting',
                entity_two_type=discograph.models.Relation.EntityType.LABEL,
                release_id=5,
                role_name='Released On',
                year=1995,
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.PRODUCTION,
                entity_one_id=22,
                entity_one_name='Datacide',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_name='Datacide',
                entity_two_type=discograph.models.Relation.EntityType.ARTIST,
                is_trivial=True,
                release_id=5,
                role_name='Producer',
                year=1995,
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.INSTRUMENTS,
                entity_one_id=25,
                entity_one_name='Tetsu Inoue',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_name='Datacide',
                entity_two_type=discograph.models.Relation.EntityType.ARTIST,
                release_id=5,
                role_name='Performer',
                subcategory=discograph.models.ArtistRole.Subcategory.OTHER_MUSICAL,
                year=1995,
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.VOCAL,
                entity_one_id=415403,
                entity_one_name='Ingrid Baier',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_name='Datacide',
                entity_two_type=discograph.models.Relation.EntityType.ARTIST,
                release_id=5,
                role_name='Voice',
                year=1995,
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.INSTRUMENTS,
                entity_one_id=519207,
                entity_one_name='Uwe Schmidt',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_name='Datacide',
                entity_two_type=discograph.models.Relation.EntityType.ARTIST,
                release_id=5,
                role_name='Performer',
                subcategory=discograph.models.ArtistRole.Subcategory.OTHER_MUSICAL,
                year=1995,
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.VISUAL,
                entity_one_id=539207,
                entity_one_name='Linger Decoree',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_name='Datacide',
                entity_two_type=discograph.models.Relation.EntityType.ARTIST,
                release_id=5,
                role_name='Cover',
                year=1995,
                )
            discograph.models.Relation(
                category=discograph.models.ArtistRole.Category.VISUAL,
                entity_one_id=539207,
                entity_one_name='Linger Decoree',
                entity_one_type=discograph.models.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_name='Datacide',
                entity_two_type=discograph.models.Relation.EntityType.ARTIST,
                release_id=5,
                role_name='Design',
                year=1995,
                )
            ''')
        assert actual == expected