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
        iterator = bootstrap.get_iterator('release')
        release_element = next(iterator)
        release_element = next(iterator)
        release_element = next(iterator)
        actual = stringtools.normalize(bootstrap.prettify(release_element))
        expected = stringtools.normalize(u'''
            <?xml version="1.0" ?>
            <release id="3" status="Accepted">
                <artists>
                    <artist>
                        <id>3</id>
                        <name>Josh Wink</name>
                        <anv/>
                        <join/>
                        <role/>
                        <tracks/>
                    </artist>
                </artists>
                <title>Profound Sounds Vol. 1</title>
                <labels>
                    <label catno="CK 63628" name="Ruffhouse Records"/>
                </labels>
                <extraartists>
                    <artist>
                        <id>3</id>
                        <name>Josh Wink</name>
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
                    <style>Techno</style>
                    <style>Tech House</style>
                </styles>
                <country>US</country>
                <released>1999-07-13</released>
                <notes>1: Track title is given as &quot;D2&quot; (which is the side of record on the vinyl version of i220-010 release). This was also released on CD where this track is listed on 8th position. On both version no titles are given (only writing/producing credits). Both versions of i220-010 can be seen on the master release page [m27265]. Additionally this track contains female vocals that aren't present on original i220-010 release.
            4: Credited as J. Dahlb\xe4ck.
            5: Track title wrongly given as &quot;Vol. 1&quot;.
            6: Credited as Gez Varley presents Tony Montana.
            12: Track exclusive to Profound Sounds Vol. 1.</notes>
                <master_id>66526</master_id>
                <data_quality>Correct</data_quality>
                <tracklist>
                    <track>
                        <position>1</position>
                        <title>Untitled 8</title>
                        <duration>7:00</duration>
                        <artists>
                            <artist>
                                <id>5</id>
                                <name>Heiko Laux</name>
                                <anv/>
                                <join>&amp;</join>
                                <role/>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>4</id>
                                <name>Johannes Heil</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>2</position>
                        <title>Anjua (Sneaky 3)</title>
                        <duration>5:28</duration>
                        <artists>
                            <artist>
                                <id>15525</id>
                                <name>Karl Axel Bissler</name>
                                <anv>K.A.B.</anv>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>3</position>
                        <title>When The Funk Hits The Fan (Mood II Swing When The Dub Hits The Fan)</title>
                        <duration>5:25</duration>
                        <artists>
                            <artist>
                                <id>7</id>
                                <name>Sylk 130</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                        <extraartists>
                            <artist>
                                <id>8</id>
                                <name>Mood II Swing</name>
                                <anv/>
                                <join/>
                                <role>Remix</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>4</position>
                        <title>What's The Time, Mr. Templar</title>
                        <duration>4:27</duration>
                        <artists>
                            <artist>
                                <id>1</id>
                                <name>Persuader, The</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>5</position>
                        <title>Vol. 2</title>
                        <duration>5:36</duration>
                        <artists>
                            <artist>
                                <id>267132</id>
                                <name>Care Company (2)</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>6</position>
                        <title>Political Prisoner</title>
                        <duration>3:37</duration>
                        <artists>
                            <artist>
                                <id>6981</id>
                                <name>Gez Varley</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>7</position>
                        <title>Pop Kulture</title>
                        <duration>5:03</duration>
                        <artists>
                            <artist>
                                <id>11</id>
                                <name>DJ Dozia</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>8</position>
                        <title>K-Mart Shopping (Hi-Fi Mix)</title>
                        <duration>5:42</duration>
                        <artists>
                            <artist>
                                <id>10702</id>
                                <name>Nerio's Dubwork</name>
                                <anv/>
                                <join>Meets</join>
                                <role/>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>233190</id>
                                <name>Kathy Lee</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                        <extraartists>
                            <artist>
                                <id>23</id>
                                <name>Alex Hi-Fi</name>
                                <anv/>
                                <join/>
                                <role>Remix</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>9</position>
                        <title>Lovelee Dae (Eight Miles High Mix)</title>
                        <duration>5:47</duration>
                        <artists>
                            <artist>
                                <id>13</id>
                                <name>Blaze</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                        <extraartists>
                            <artist>
                                <id>14</id>
                                <name>Eight Miles High</name>
                                <anv/>
                                <join/>
                                <role>Remix</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>10</position>
                        <title>Sweat</title>
                        <duration>6:06</duration>
                        <artists>
                            <artist>
                                <id>67226</id>
                                <name>Stacey Pullen</name>
                                <anv/>
                                <join>Presents</join>
                                <role/>
                                <tracks/>
                            </artist>
                            <artist>
                                <id>7554</id>
                                <name>Black Odyssey</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                        <extraartists>
                            <artist>
                                <id>67226</id>
                                <name>Stacey Pullen</name>
                                <anv/>
                                <join/>
                                <role>Presenter</role>
                                <tracks/>
                            </artist>
                        </extraartists>
                    </track>
                    <track>
                        <position>11</position>
                        <title>Silver</title>
                        <duration>3:16</duration>
                        <artists>
                            <artist>
                                <id>3906</id>
                                <name>Christian Smith &amp; John Selway</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>12</position>
                        <title>Untitled</title>
                        <duration>2:46</duration>
                        <artists>
                            <artist>
                                <id>3</id>
                                <name>Josh Wink</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>13</position>
                        <title>Boom Box</title>
                        <duration>3:41</duration>
                        <artists>
                            <artist>
                                <id>19</id>
                                <name>Sound Associates</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                    <track>
                        <position>14</position>
                        <title>Track 2</title>
                        <duration>3:39</duration>
                        <artists>
                            <artist>
                                <id>20</id>
                                <name>Percy X</name>
                                <anv/>
                                <join>,</join>
                                <role/>
                                <tracks/>
                            </artist>
                        </artists>
                    </track>
                </tracklist>
                <identifiers>
                    <identifier type="Barcode" value="074646362822"/>
                </identifiers>
                <companies>
                    <company>
                        <id>93330</id>
                        <name>Columbia Records</name>
                        <catno/>
                        <entity_type>10</entity_type>
                        <entity_type_name>Manufactured By</entity_type_name>
                        <resource_url>http://api.discogs.com/labels/93330</resource_url>
                    </company>
                    <company>
                        <id>93330</id>
                        <name>Columbia Records</name>
                        <catno/>
                        <entity_type>9</entity_type>
                        <entity_type_name>Distributed By</entity_type_name>
                        <resource_url>http://api.discogs.com/labels/93330</resource_url>
                    </company>
                </companies>
            </release>
            ''')
        assert actual.splitlines() == expected.splitlines()
        release_document = models.Release.from_element(release_element)
        actual = format(release_document)
        expected = stringtools.normalize(u'''
            discograph.models.Release(
                artists=[
                    discograph.models.ArtistCredit(
                        artist=discograph.models.Artist(
                            aliases=[],
                            discogs_id=3,
                            has_been_scraped=False,
                            members=[],
                            name=u'Josh Wink',
                            name_variations=[],
                            ),
                        ),
                    ],
                companies=[],
                country=u'US',
                data_quality=u'Correct',
                extra_artists=[
                    discograph.models.ArtistCredit(
                        artist=discograph.models.Artist(
                            aliases=[],
                            discogs_id=3,
                            has_been_scraped=False,
                            members=[],
                            name=u'Josh Wink',
                            name_variations=[],
                            ),
                        role=u'DJ Mix',
                        ),
                    ],
                formats=[
                    discograph.models.Format(
                        descriptions=[
                            u'Compilation',
                            u'Mixed',
                            ],
                        name=u'CD',
                        quantity=1,
                        ),
                    ],
                genres=[
                    u'Electronic',
                    ],
                identifiers=[
                    discograph.models.Identifier(
                        type_=u'Barcode',
                        value=u'074646362822',
                        ),
                    ],
                labels=[],
                styles=[
                    u'Techno',
                    u'Tech House',
                    ],
                title=u'Profound Sounds Vol. 1',
                tracklist=[],
                )
            ''')
        assert actual == expected