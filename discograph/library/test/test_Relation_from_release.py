# -*- encoding: utf-8 -*-
import mongoengine
import unittest
from abjad.tools import stringtools
from discograph.library.Bootstrapper import Bootstrapper
from discograph import library
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree


class Test(unittest.TestCase):

    database_name = 'discograph-test'

    def setUp(self):
        self.database = mongoengine.connect(self.database_name)

    def tearDown(self):
        self.database.drop_database(self.database_name)
        self.database.close()

    def test_01(self):
        iterator = Bootstrapper.get_iterator('release')
        release_element = next(iterator)
        release_document = library.Release.from_element(release_element)
        release_document.resolve_references(spuriously=True)
        relations = library.Relation.from_release(release_document)
        actual = '\n'.join(format(_) for _ in relations)
        expected = stringtools.normalize(r'''
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.RELATION,
                country='Sweden',
                entity_one_id=1,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=-3,
                entity_two_type=discograph.library.Relation.EntityType.LABEL,
                genres=['Electronic'],
                release_id=1,
                role_name='Released On',
                styles=['Deep House'],
                year=1999,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.WRITING_AND_ARRANGEMENT,
                country='Sweden',
                entity_one_id=239,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=1,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=1,
                role_name='Music By',
                styles=['Deep House'],
                year=1999,
                )
            ''')
        assert actual == expected

    @unittest.skip('Labels not constructed by Relation.from_release().')
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
        release_document = library.Release.from_element(release_element)
        relations = library.Relation.from_release(release_document)
        actual = '\n'.join(format(_) for _ in relations)
        expected = stringtools.normalize(r'''
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.RELATION,
                entity_one_id=195,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_type=discograph.library.Relation.EntityType.LABEL,
                release_id=103,
                role_name='Compiled On',
                year=1999,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.RELATION,
                entity_one_id=196,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_type=discograph.library.Relation.EntityType.LABEL,
                release_id=103,
                role_name='Compiled On',
                year=1999,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.RELATION,
                entity_one_id=197,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_type=discograph.library.Relation.EntityType.LABEL,
                release_id=103,
                role_name='Compiled On',
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
        release_document = library.Release.from_element(release_element)
        relations = library.Relation.from_release(release_document)
        actual = '\n'.join(format(_) for _ in relations)
        expected = stringtools.normalize(r'''
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.PRODUCTION,
                country='Germany',
                entity_one_id=22,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=5,
                role_name='Producer',
                styles=['Abstract', 'Ambient'],
                year=1995,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.INSTRUMENTS,
                country='Germany',
                entity_one_id=25,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=5,
                role_name='Performer',
                styles=['Abstract', 'Ambient'],
                subcategory=discograph.library.ArtistRole.Subcategory.OTHER_MUSICAL,
                year=1995,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.VOCAL,
                country='Germany',
                entity_one_id=415403,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=5,
                role_name='Voice',
                styles=['Abstract', 'Ambient'],
                year=1995,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.INSTRUMENTS,
                country='Germany',
                entity_one_id=519207,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=5,
                role_name='Performer',
                styles=['Abstract', 'Ambient'],
                subcategory=discograph.library.ArtistRole.Subcategory.OTHER_MUSICAL,
                year=1995,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.VISUAL,
                country='Germany',
                entity_one_id=539207,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=5,
                role_name='Cover',
                styles=['Abstract', 'Ambient'],
                year=1995,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.VISUAL,
                country='Germany',
                entity_one_id=539207,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=22,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=5,
                role_name='Design',
                styles=['Abstract', 'Ambient'],
                year=1995,
                )
            ''')
        assert actual == expected

    def test_04(self):
        source = stringtools.normalize(r"""
            <?xml version="1.0" ?>
            <release id="36" status="Accepted">
                <artists>
                    <artist>
                        <id>64</id>
                        <name>Christopher Lawrence</name>
                        <anv/>
                        <join/>
                        <role/>
                        <tracks/>
                    </artist>
                </artists>
                <title>Trilogy, Part One: Empire</title>
                <labels>
                    <label catno="MM 80123-2" name="Moonshine Music"/>
                </labels>
                <extraartists>
                    <artist>
                        <id>64</id>
                        <name>Christopher Lawrence</name>
                        <anv/>
                        <join/>
                        <role>DJ Mix</role>
                        <tracks/>
                    </artist>
                </extraartists>
                <formats>
                    <format name="CD" qty="1" text="">
                        <descriptions>
                            <description>Compilation</description>
                            <description>Mixed</description>
                        </descriptions>
                    </format>
                </formats>
                <genres>
                    <genre>Electronic</genre>
                </genres>
                <styles>
                    <style>Trance</style>
                </styles>
                <country>US</country>
                <released>2000-00-00</released>
                <notes>This compilation ℗ © 2000 Moonshine Music
            Made in the USA.
            </notes>
                <data_quality>Correct</data_quality>
                <tracklist>
                    <track>
                        <position>1</position>
                        <title>Persuasion (Animated Mix)</title>
                        <duration/>
                        <artists>
                            <artist>
                                <id>65</id>
                                <name>Animated Rhythm</name>
                                <anv/>
                                <join/>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>2</position>
                        <title>Eterna</title>
                        <duration/>
                        <artists>
                            <artist>
                                <id>66</id>
                                <name>Christian West</name>
                                <anv/>
                                <join/>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>3</position>
                        <title>Implode</title>
                        <duration/>
                        <artists>
                            <artist>
                                <id>67</id>
                                <name>Cassidy</name>
                                <anv/>
                                <join/>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>4</position>
                        <title>Slowburn</title>
                        <duration/>
                        <artists>
                            <artist>
                                <id>222489</id>
                                <name>Icon (9)</name>
                                <anv/>
                                <join>Featuring</join>
                                <role/>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>36400</id>
                                <name>DJ Oberon</name>
                                <anv/>
                                <join/>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                        <extraartists>
                            <artist>
                                <id>36400</id>
                                <name>DJ Oberon</name>
                                <anv/>
                                <join/>
                                <role>Featuring</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>5</position>
                        <title>Colossus</title>
                        <duration/>
                        <artists>
                            <artist>
                                <id>69</id>
                                <name>Sound System, The</name>
                                <anv/>
                                <join/>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>6</position>
                        <title>Rhythm Of Life (Trance Mix)</title>
                        <duration/>
                        <artists>
                            <artist>
                                <id>70</id>
                                <name>Secret, The</name>
                                <anv/>
                                <join/>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>7</position>
                        <title>Hard Work</title>
                        <duration/>
                        <artists>
                            <artist>
                                <id>71</id>
                                <name>Baby Doc</name>
                                <anv/>
                                <join/>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>8</position>
                        <title>Renegade</title>
                        <duration/>
                        <artists>
                            <artist>
                                <id>64</id>
                                <name>Christopher Lawrence</name>
                                <anv/>
                                <join/>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>9</position>
                        <title>Twin Town</title>
                        <duration/>
                        <artists>
                            <artist>
                                <id>4210</id>
                                <name>Ian Wilkie</name>
                                <anv/>
                                <join>Vs.</join>
                                <role/>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>1014</id>
                                <name>Timo Maas</name>
                                <anv/>
                                <join/>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>10</position>
                        <title>Bubble &amp; Squeak</title>
                        <duration/>
                        <artists>
                            <artist>
                                <id>71</id>
                                <name>Baby Doc</name>
                                <anv/>
                                <join/>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>11</position>
                        <title>Rush Hour</title>
                        <duration/>
                        <artists>
                            <artist>
                                <id>64</id>
                                <name>Christopher Lawrence</name>
                                <anv/>
                                <join/>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                </tracklist>
                <identifiers>
                    <identifier type="Barcode" value="785688012322"/>
                </identifiers>
                <companies/>
            </release>
            """)
        release_element = ElementTree.fromstring(source)
        release_document = library.Release.from_element(release_element)
        relations = library.Relation.from_release(release_document)
        actual = '\n'.join(format(_) for _ in relations)
        expected = stringtools.normalize(r"""
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.DJ_MIX,
                country='US',
                entity_one_id=64,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=64,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='DJ Mix',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.DJ_MIX,
                country='US',
                entity_one_id=64,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=65,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='DJ Mix',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.DJ_MIX,
                country='US',
                entity_one_id=64,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=66,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='DJ Mix',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.DJ_MIX,
                country='US',
                entity_one_id=64,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=67,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='DJ Mix',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.DJ_MIX,
                country='US',
                entity_one_id=64,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=69,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='DJ Mix',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.DJ_MIX,
                country='US',
                entity_one_id=64,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=70,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='DJ Mix',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.DJ_MIX,
                country='US',
                entity_one_id=64,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=71,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='DJ Mix',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.DJ_MIX,
                country='US',
                entity_one_id=64,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=1014,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='DJ Mix',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.DJ_MIX,
                country='US',
                entity_one_id=64,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=4210,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='DJ Mix',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.DJ_MIX,
                country='US',
                entity_one_id=64,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=36400,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='DJ Mix',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.DJ_MIX,
                country='US',
                entity_one_id=64,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=222489,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='DJ Mix',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.FEATURING_AND_PRESENTING,
                country='US',
                entity_one_id=36400,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=36400,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='Featuring',
                styles=['Trance'],
                year=2000,
                )
            discograph.library.Relation(
                category=discograph.library.ArtistRole.Category.FEATURING_AND_PRESENTING,
                country='US',
                entity_one_id=36400,
                entity_one_type=discograph.library.Relation.EntityType.ARTIST,
                entity_two_id=222489,
                entity_two_type=discograph.library.Relation.EntityType.ARTIST,
                genres=['Electronic'],
                release_id=36,
                role_name='Featuring',
                styles=['Trance'],
                year=2000,
                )
            """)
        assert actual == expected