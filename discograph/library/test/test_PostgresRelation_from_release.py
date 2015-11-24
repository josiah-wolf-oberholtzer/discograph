# -*- encoding: utf-8 -*-
import discograph
from abjad.tools import stringtools
from discograph.library.Bootstrapper import Bootstrapper
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree


class Test(discograph.DiscographTestCase):

    def test_01(self):
        iterator = Bootstrapper.get_iterator('release')
        release_element = next(iterator)
        release_document = discograph.PostgresRelease.from_element(release_element)
        release_document.resolve_references({}, spuriously=True)
        actual = discograph.PostgresRelation.from_release(release_document)
        expected = [
            {
                'entity_one_id': 1,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 56025,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 1,
                'role': 'Pressed By',
                'year': 1999,
                },
            {
                'entity_one_id': 1,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 271046,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 1,
                'role': 'Recorded At',
                'year': 1999,
                },
            {
                'entity_one_id': 1,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': -1,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 1,
                'role': 'Released On',
                'year': 1999,
                },
            {
                'entity_one_id': 239,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 1,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 1,
                'role': 'Music By',
                'year': 1999,
                },
            ]
        assert actual == expected

    #@unittest.skip('Labels not constructed by Relation.from_release().')
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
        release_document = discograph.PostgresRelease.from_element(release_element)
        release_document.resolve_references({}, spuriously=True)
        actual = discograph.PostgresRelation.from_release(release_document)
        expected = [
            {
                'entity_one_id': 195,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': -1,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 103,
                'role': 'Compiled On',
                'year': 1999,
                },
            {
                'entity_one_id': 196,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': -1,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 103,
                'role': 'Compiled On',
                'year': 1999,
                },
            {
                'entity_one_id': 197,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': -1,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 103,
                'role': 'Compiled On',
                'year': 1999,
                },
            ]
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
        release_document = discograph.PostgresRelease.from_element(release_element)
        release_document.resolve_references({}, spuriously=True)
        actual = discograph.PostgresRelation.from_release(release_document)
        expected = [
            {
                'entity_one_id': 22,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 291931,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 5,
                'role': 'Manufactured By',
                'year': 1995,
                },
            {
                'entity_one_id': 22,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 403521,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 5,
                'role': 'Marketed By',
                'year': 1995,
                },
            {
                'entity_one_id': 22,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 265233,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 5,
                'role': 'Produced At',
                'year': 1995,
                },
            {
                'entity_one_id': 22,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 22,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 5,
                'role': 'Producer',
                'year': 1995,
                },
            {
                'entity_one_id': 22,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': -1,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 5,
                'role': 'Released On',
                'year': 1995,
                },
            {
                'entity_one_id': 25,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 22,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 5,
                'role': 'Performer',
                'year': 1995,
                },
            {
                'entity_one_id': 415403,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 22,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 5,
                'role': 'Voice',
                'year': 1995,
                },
            {
                'entity_one_id': 519207,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 22,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 5,
                'role': 'Performer',
                'year': 1995,
                },
            {
                'entity_one_id': 539207,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 22,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 5,
                'role': 'Cover',
                'year': 1995,
                },
            {
                'entity_one_id': 539207,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 22,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 5,
                'role': 'Design',
                'year': 1995,
                },
            ]
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
        release_document = discograph.PostgresRelease.from_element(release_element)
        release_document.resolve_references({}, spuriously=True)
        actual = discograph.PostgresRelation.from_release(release_document)
        expected = [
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 64,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'DJ Mix',
                'year': 2000,
                },
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 65,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'DJ Mix',
                'year': 2000,
                },
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 66,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'DJ Mix',
                'year': 2000,
                },
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 67,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'DJ Mix',
                'year': 2000,
                },
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 69,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'DJ Mix',
                'year': 2000,
                },
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 70,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'DJ Mix',
                'year': 2000,
                },
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 71,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'DJ Mix',
                'year': 2000,
                },
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 1014,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'DJ Mix',
                'year': 2000,
                },
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 4210,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'DJ Mix',
                'year': 2000,
                },
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 36400,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'DJ Mix',
                'year': 2000,
                },
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 222489,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'DJ Mix',
                'year': 2000,
                },
            {
                'entity_one_id': 64,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': -1,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 36,
                'role': 'Released On',
                'year': 2000,
                },
            {
                'entity_one_id': 36400,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 36400,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'Featuring',
                'year': 2000,
                },
            {
                'entity_one_id': 36400,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 222489,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 36,
                'role': 'Featuring',
                'year': 2000,
                },
            ]
        assert actual == expected

    def test_05(self):
        source = stringtools.normalize(r'''
            <?xml version="1.0" ?>
            <release id="3286" status="Accepted">
                <artists>
                    <artist>
                        <id>21</id>
                        <name>Faze Action</name>
                        <anv/>
                        <join/>
                        <role/>
                        <tracks/>
                    </artist>
                </artists>
                <title>Moving Cities</title>
                <labels>
                    <label catno="NUX 139CD" name="Nuphonic"/>
                </labels>
                <extraartists>
                    <artist>
                        <id>1832523</id>
                        <name>Tom Hingston Studio</name>
                        <anv/>
                        <join/>
                        <role>Artwork By [Design]</role>
                        <tracks/>
                    </artist>
                    <artist>
                        <id>246316</id>
                        <name>Raj Gupta</name>
                        <anv/>
                        <join/>
                        <role>Edited By</role>
                        <tracks/>
                    </artist>
                    <artist>
                        <id>246316</id>
                        <name>Raj Gupta</name>
                        <anv/>
                        <join/>
                        <role>Engineer [Recording And Mixing]</role>
                        <tracks>2 to 11</tracks>
                    </artist>
                    <artist>
                        <id>364438</id>
                        <name>Martin Giles</name>
                        <anv/>
                        <join/>
                        <role>Mastered By</role>
                        <tracks/>
                    </artist>
                    <artist>
                        <id>388361</id>
                        <name>Mike Brown (3)</name>
                        <anv/>
                        <join/>
                        <role>Mastered By</role>
                        <tracks/>
                    </artist>
                    <artist>
                        <id>86765</id>
                        <name>Richard Green</name>
                        <anv/>
                        <join/>
                        <role>Photography</role>
                        <tracks/>
                    </artist>
                    <artist>
                        <id>56668</id>
                        <name>Zeke Manyika</name>
                        <anv/>
                        <join/>
                        <role>Vocals</role>
                        <tracks>2, 4, 5, 8</tracks>
                    </artist>
                    <artist>
                        <id>308472</id>
                        <name>Robin Lee</name>
                        <anv/>
                        <join/>
                        <role>Written-By</role>
                        <tracks/>
                    </artist>
                    <artist>
                        <id>133484</id>
                        <name>Simon Lee</name>
                        <anv/>
                        <join/>
                        <role>Written-By</role>
                        <tracks/>
                    </artist>
                    <artist>
                        <id>56668</id>
                        <name>Zeke Manyika</name>
                        <anv/>
                        <join/>
                        <role>Written-By</role>
                        <tracks>1 to 9, 11</tracks>
                    </artist>
                </extraartists>
                <formats>
                    <format name="CD" qty="1" text="">
                        <descriptions>
                            <description>Album</description>
                        </descriptions>
                    </format>
                </formats>
                <genres>
                    <genre>Electronic</genre>
                </genres>
                <styles>
                    <style>Deep House</style>
                </styles>
                <country>UK</country>
                <released>1999-09-27</released>
                <notes>Comes in a jewel case with transparent tray.

            All tracks recorded and mixed at Laj Studios on a Digidesign system.
            Except: Track 1, recorded at Can Can Studios.
            Mastered at CTS Mastering, London.
            ℗ &amp; © 1999 Nuphonic
            Distributed by Vital T.
            </notes>
                <master_id>104980</master_id>
                <data_quality>Correct</data_quality>
                <tracklist>
                    <track>
                        <position>1</position>
                        <title>Isis</title>
                        <duration>5:39</duration>
                        <extraartists>
                            <artist>
                                <id>308472</id>
                                <name>Robin Lee</name>
                                <anv/>
                                <join/>
                                <role>Bass, Cello, Keyboards</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>13481</id>
                                <name>Ben Mitchell</name>
                                <anv/>
                                <join/>
                                <role>Engineer [Recording And Mixing]</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>2</position>
                        <title>To Love Is To Grow</title>
                        <duration>5:15</duration>
                        <extraartists>
                            <artist>
                                <id>12601</id>
                                <name>Tim Hutton</name>
                                <anv/>
                                <join/>
                                <role>Guitar</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>246316</id>
                                <name>Raj Gupta</name>
                                <anv/>
                                <join/>
                                <role>Programmed By [Additional]</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>308472</id>
                                <name>Robin Lee</name>
                                <anv/>
                                <join/>
                                <role>Programmed By [Additional], Bass</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>246316</id>
                                <name>Raj Gupta</name>
                                <anv/>
                                <join/>
                                <role>Written-By</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>56668</id>
                                <name>Zeke Manyika</name>
                                <anv/>
                                <join/>
                                <role>Written-By</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>3</position>
                        <title>Samba</title>
                        <duration>5:57</duration>
                        <extraartists>
                            <artist>
                                <id>308472</id>
                                <name>Robin Lee</name>
                                <anv/>
                                <join/>
                                <role>Bass, Keyboards</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>328648</id>
                                <name>Richard Wargent</name>
                                <anv/>
                                <join/>
                                <role>Flute</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>12601</id>
                                <name>Tim Hutton</name>
                                <anv/>
                                <join/>
                                <role>Guitar</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>328648</id>
                                <name>Richard Wargent</name>
                                <anv/>
                                <join/>
                                <role>Saxophone</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>402322</id>
                                <name>Andrew Watson</name>
                                <anv/>
                                <join/>
                                <role>Trombone</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>402324</id>
                                <name>Lee Vivien</name>
                                <anv/>
                                <join/>
                                <role>Trumpet</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>4</position>
                        <title>Got To Find A Way</title>
                        <duration>5:46</duration>
                        <extraartists>
                            <artist>
                                <id>308472</id>
                                <name>Robin Lee</name>
                                <anv/>
                                <join/>
                                <role>Bass, Keyboards</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>156648</id>
                                <name>Brian Wright</name>
                                <anv/>
                                <join/>
                                <role>Viola</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>156648</id>
                                <name>Brian Wright</name>
                                <anv/>
                                <join/>
                                <role>Violin</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>56668</id>
                                <name>Zeke Manyika</name>
                                <anv/>
                                <join/>
                                <role>Written-By</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>5</position>
                        <title>Kariba</title>
                        <duration>5:13</duration>
                        <extraartists>
                            <artist>
                                <id>308472</id>
                                <name>Robin Lee</name>
                                <anv/>
                                <join/>
                                <role>Bass, Keyboards, Percussion</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>328648</id>
                                <name>Richard Wargent</name>
                                <anv/>
                                <join/>
                                <role>Flute</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>246316</id>
                                <name>Raj Gupta</name>
                                <anv/>
                                <join/>
                                <role>Percussion</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>56668</id>
                                <name>Zeke Manyika</name>
                                <anv/>
                                <join/>
                                <role>Percussion</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>328648</id>
                                <name>Richard Wargent</name>
                                <anv/>
                                <join/>
                                <role>Saxophone</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>402322</id>
                                <name>Andrew Watson</name>
                                <anv/>
                                <join/>
                                <role>Trombone</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>402324</id>
                                <name>Lee Vivien</name>
                                <anv/>
                                <join/>
                                <role>Trumpet</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>56668</id>
                                <name>Zeke Manyika</name>
                                <anv/>
                                <join/>
                                <role>Written-By</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>6</position>
                        <title>Space Disco</title>
                        <duration>6:42</duration>
                        <extraartists>
                            <artist>
                                <id>308472</id>
                                <name>Robin Lee</name>
                                <anv/>
                                <join/>
                                <role>Bass, Keyboards</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>402323</id>
                                <name>Darian McCarthy</name>
                                <anv/>
                                <join/>
                                <role>Guitar</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>383869</id>
                                <name>Basil Isaac</name>
                                <anv/>
                                <join/>
                                <role>Percussion</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>7</position>
                        <title>Moving Cities</title>
                        <duration>6:24</duration>
                        <extraartists>
                            <artist>
                                <id>308472</id>
                                <name>Robin Lee</name>
                                <anv/>
                                <join/>
                                <role>Bass, Keyboards, Cello</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>330312</id>
                                <name>Andy Waterworth</name>
                                <anv/>
                                <join/>
                                <role>Double Bass</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>392454</id>
                                <name>Pim Jones</name>
                                <anv/>
                                <join/>
                                <role>Guitar</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>156648</id>
                                <name>Brian Wright</name>
                                <anv/>
                                <join/>
                                <role>Viola</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>156648</id>
                                <name>Brian Wright</name>
                                <anv/>
                                <join/>
                                <role>Violin</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>8</position>
                        <title>Mas</title>
                        <duration>5:56</duration>
                        <extraartists>
                            <artist>
                                <id>308472</id>
                                <name>Robin Lee</name>
                                <anv/>
                                <join/>
                                <role>Bass</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>402325</id>
                                <name>William Kingswood</name>
                                <anv/>
                                <join/>
                                <role>Guitar</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>31885</id>
                                <name>Pete Z.</name>
                                <anv/>
                                <join/>
                                <role>Keyboards</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>9</position>
                        <title>Horizons</title>
                        <duration>5:10</duration>
                        <extraartists>
                            <artist>
                                <id>133484</id>
                                <name>Simon Lee</name>
                                <anv/>
                                <join/>
                                <role>Effects [Vocoder]</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>246316</id>
                                <name>Raj Gupta</name>
                                <anv/>
                                <join/>
                                <role>Programmed By [Additional]</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>308472</id>
                                <name>Robin Lee</name>
                                <anv/>
                                <join/>
                                <role>Programmed By, Keyboards, Effects [Vocoder]</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>10</position>
                        <title>Heartbeat</title>
                        <duration>5:45</duration>
                        <extraartists>
                            <artist>
                                <id>308472</id>
                                <name>Robin Lee</name>
                                <anv/>
                                <join/>
                                <role>Guitar, Bass, Keyboards</role>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>9559</id>
                                <name>Vanessa Freeman</name>
                                <anv/>
                                <join/>
                                <role>Vocals, Written-By</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>11</position>
                        <title>A Day To Go</title>
                        <duration>5:31</duration>
                        <extraartists>
                            <artist>
                                <id>308472</id>
                                <name>Robin Lee</name>
                                <anv/>
                                <join/>
                                <role>Bass, Keyboards</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                </tracklist>
                <identifiers>
                    <identifier type="Barcode" value="0 675601 139024"/>
                    <identifier type="Matrix / Runout" value="IMPRESS NUX139CD 01 6   MADE IN UK BY PMDC"/>
                    <identifier description="SID Codes" type="Other" value="IFPI L136 &amp; IFPI 0490"/>
                </identifiers>
                <videos>
                    <video duration="102" embed="true" src="http://www.youtube.com/watch?v=hI8TsbpV-l4">
                        <title>To Love is to Grow '99</title>
                        <description>To Love is to Grow '99</description>
                    </video>
                    <video duration="313" embed="true" src="http://www.youtube.com/watch?v=DkI1HPGxfZo">
                        <title>(1999) Faze Action feat. Zeke Manyika - Kariba [Album Mix]</title>
                        <description>(1999) Faze Action feat. Zeke Manyika - Kariba [Album Mix]</description>
                    </video>
                    <video duration="402" embed="true" src="http://www.youtube.com/watch?v=0krTFONiztY">
                        <title>Faze Action - Moving Cities</title>
                        <description>Faze Action - Moving Cities</description>
                    </video>
                </videos>
                <companies/>
            </release>
            ''')
        release_element = ElementTree.fromstring(source)
        release_document = discograph.PostgresRelease.from_element(release_element)
        release_document.resolve_references({}, spuriously=True)
        actual = discograph.PostgresRelation.from_release(release_document)
        expected = [
            {
                'entity_one_id': 21,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': -1,
                'entity_two_type': discograph.PostgresRelation.EntityType.LABEL,
                'release_id': 3286,
                'role': 'Released On',
                'year': 1999,
                },
            {
                'entity_one_id': 9559,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Vocals',
                'year': 1999,
                },
            {
                'entity_one_id': 9559,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Written-By',
                'year': 1999,
                },
            {
                'entity_one_id': 12601,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Guitar',
                'year': 1999,
                },
            {
                'entity_one_id': 13481,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Engineer',
                'year': 1999,
                },
            {
                'entity_one_id': 31885,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Keyboards',
                'year': 1999,
                },
            {
                'entity_one_id': 56668,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Percussion',
                'year': 1999,
                },
            {
                'entity_one_id': 56668,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Vocals',
                'year': 1999,
                },
            {
                'entity_one_id': 56668,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Written-By',
                'year': 1999,
                },
            {
                'entity_one_id': 86765,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Photography',
                'year': 1999,
                },
            {
                'entity_one_id': 133484,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Effects',
                'year': 1999,
                },
            {
                'entity_one_id': 133484,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Written-By',
                'year': 1999,
                },
            {
                'entity_one_id': 156648,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Viola',
                'year': 1999,
                },
            {
                'entity_one_id': 156648,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Violin',
                'year': 1999,
                },
            {
                'entity_one_id': 246316,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Edited By',
                'year': 1999,
                },
            {
                'entity_one_id': 246316,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Engineer',
                'year': 1999,
                },
            {
                'entity_one_id': 246316,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Percussion',
                'year': 1999,
                },
            {
                'entity_one_id': 246316,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Programmed By',
                'year': 1999,
                },
            {
                'entity_one_id': 246316,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Written-By',
                'year': 1999,
                },
            {
                'entity_one_id': 308472,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Bass',
                'year': 1999,
                },
            {
                'entity_one_id': 308472,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Cello',
                'year': 1999,
                },
            {
                'entity_one_id': 308472,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Effects',
                'year': 1999,
                },
            {
                'entity_one_id': 308472,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Guitar',
                'year': 1999,
                },
            {
                'entity_one_id': 308472,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Keyboards',
                'year': 1999,
                },
            {
                'entity_one_id': 308472,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Percussion',
                'year': 1999,
                },
            {
                'entity_one_id': 308472,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Programmed By',
                'year': 1999,
                },
            {
                'entity_one_id': 308472,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Written-By',
                'year': 1999,
                },
            {
                'entity_one_id': 328648,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Flute',
                'year': 1999,
                },
            {
                'entity_one_id': 328648,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Saxophone',
                'year': 1999,
                },
            {
                'entity_one_id': 330312,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Double Bass',
                'year': 1999,
                },
            {
                'entity_one_id': 364438,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Mastered By',
                'year': 1999,
                },
            {
                'entity_one_id': 383869,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Percussion',
                'year': 1999,
                },
            {
                'entity_one_id': 388361,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Mastered By',
                'year': 1999,
                },
            {
                'entity_one_id': 392454,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Guitar',
                'year': 1999,
                },
            {
                'entity_one_id': 402322,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Trombone',
                'year': 1999,
                },
            {
                'entity_one_id': 402323,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Guitar',
                'year': 1999,
                },
            {
                'entity_one_id': 402324,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Trumpet',
                'year': 1999,
                },
            {
                'entity_one_id': 402325,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Guitar',
                'year': 1999,
                },
            {
                'entity_one_id': 1832523,
                'entity_one_type': discograph.PostgresRelation.EntityType.ARTIST,
                'entity_two_id': 21,
                'entity_two_type': discograph.PostgresRelation.EntityType.ARTIST,
                'release_id': 3286,
                'role': 'Artwork By',
                'year': 1999,
                },
            ]
        assert actual == expected
