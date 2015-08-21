# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import mongoengine.connection
import unittest
from abjad import stringtools
from discograph import bootstrap
from discograph import models


class Test(unittest.TestCase):

    database_name = 'discograph:test'

    def setUp(self):
        self.database = mongoengine.connect(self.database_name)

    def tearDown(self):
        self.database.drop_database(self.database_name)
        self.database.close()

    def test_01(self):
        iterator = bootstrap.get_iterator('release')
        release_element = next(iterator)
        actual = stringtools.normalize(bootstrap.prettify(release_element))
        expected = stringtools.normalize(u'''
            <?xml version="1.0" ?>
            <release id="1" status="Accepted">
                <artists>
                    <artist>
                        <id>1</id>
                        <name>Persuader, The</name>
                        <anv/>
                        <join/>
                        <role/>
                        <tracks/>
                    </artist>
                </artists>
                <title>Stockholm</title>
                <labels>
                    <label catno="SK032" name="Svek"/>
                </labels>
                <extraartists>
                    <artist>
                        <id>239</id>
                        <name>Jesper Dahlb\xe4ck</name>
                        <anv/>
                        <join/>
                        <role>Music By [All Tracks By]</role>
                        <tracks/>
                    </artist>
                </extraartists>
                <formats>
                    <format name="Vinyl" qty="2" text="">
                        <descriptions>
                            <description>12&quot;</description>
                            <description>33 \u2153 RPM</description>
                        </descriptions>
                    </format>
                </formats>
                <genres>
                    <genre>Electronic</genre>
                </genres>
                <styles>
                    <style>Deep House</style>
                </styles>
                <country>Sweden</country>
                <released>1999-03-00</released>
                <notes>The song titles are the names of Stockholm's districts.
            </notes>
                <data_quality>Complete and Correct</data_quality>
                <tracklist>
                    <track>
                        <position>A</position>
                        <title>\xd6stermalm</title>
                        <duration>4:45</duration>
                    </track>
                    <track>
                        <position>B1</position>
                        <title>Vasastaden</title>
                        <duration>6:11</duration>
                    </track>
                    <track>
                        <position>B2</position>
                        <title>Kungsholmen</title>
                        <duration>2:49</duration>
                    </track>
                    <track>
                        <position>C1</position>
                        <title>S\xf6dermalm</title>
                        <duration>5:38</duration>
                    </track>
                    <track>
                        <position>C2</position>
                        <title>Norrmalm</title>
                        <duration>4:52</duration>
                    </track>
                    <track>
                        <position>D</position>
                        <title>Gamla Stan</title>
                        <duration>5:16</duration>
                    </track>
                </tracklist>
                <identifiers>
                    <identifier description="A-Side" type="Matrix / Runout" value="MPO SK 032 A1 G PHRUPMASTERGENERAL T27 LONDON"/>
                    <identifier description="B-Side" type="Matrix / Runout" value="MPO SK 032 B1"/>
                    <identifier description="C-Side" type="Matrix / Runout" value="MPO SK 032 C1"/>
                    <identifier description="D-Side" type="Matrix / Runout" value="MPO SK 032 D1"/>
                </identifiers>
                <videos>
                    <video duration="290" embed="true" src="http://www.youtube.com/watch?v=AHuQWcylaU4">
                        <title>The Persuader (Jesper Dahlb\xe4ck) - \xd6stermalm</title>
                        <description>The Persuader (Jesper Dahlb\xe4ck) - \xd6stermalm</description>
                    </video>
                    <video duration="380" embed="true" src="http://www.youtube.com/watch?v=5rA8CTKKEP4">
                        <title>The Persuader - Vasastaden</title>
                        <description>The Persuader - Vasastaden</description>
                    </video>
                    <video duration="335" embed="true" src="http://www.youtube.com/watch?v=QVdDhOnoR8k">
                        <title>The Persuader-Stockholm-Sodermalm</title>
                        <description>The Persuader-Stockholm-Sodermalm</description>
                    </video>
                    <video duration="289" embed="true" src="http://www.youtube.com/watch?v=hy47qgyJeG0">
                        <title>The Persuader - Norrmalm</title>
                        <description>The Persuader - Norrmalm</description>
                    </video>
                </videos>
                <companies>
                    <company>
                        <id>271046</id>
                        <name>The Globe Studios</name>
                        <catno/>
                        <entity_type>23</entity_type>
                        <entity_type_name>Recorded At</entity_type_name>
                        <resource_url>http://api.discogs.com/labels/271046</resource_url>
                    </company>
                    <company>
                        <id>56025</id>
                        <name>MPO</name>
                        <catno/>
                        <entity_type>17</entity_type>
                        <entity_type_name>Pressed By</entity_type_name>
                        <resource_url>http://api.discogs.com/labels/56025</resource_url>
                    </company>
                </companies>
            </release>
            ''')
        assert actual.splitlines() == expected.splitlines()
        release_document = models.Release.from_element(release_element)
        actual = format(release_document)
        expected = stringtools.normalize(u"""
            discograph.models.Release(
                artists=[
                    discograph.models.ArtistCredit(
                        artist=discograph.models.Artist(
                            aliases=[],
                            discogs_id=1,
                            has_been_scraped=False,
                            members=[],
                            name=u'Persuader, The',
                            name_variations=[],
                            ),
                        ),
                    ],
                companies=[
                    discograph.models.CompanyCredit(
                        company=discograph.models.Label(
                            has_been_scraped=False,
                            name=u'The Globe Studios',
                            sublabels=[],
                            ),
                        entity_type=23,
                        entity_type_name=u'Recorded At',
                        ),
                    discograph.models.CompanyCredit(
                        company=discograph.models.Label(
                            has_been_scraped=False,
                            name=u'MPO',
                            sublabels=[],
                            ),
                        entity_type=17,
                        entity_type_name=u'Pressed By',
                        ),
                    ],
                country=u'Sweden',
                data_quality=u'Complete and Correct',
                discogs_id=1,
                extra_artists=[
                    discograph.models.ArtistCredit(
                        artist=discograph.models.Artist(
                            aliases=[],
                            discogs_id=239,
                            has_been_scraped=False,
                            members=[],
                            name=u'Jesper Dahlb\\xe4ck',
                            name_variations=[],
                            ),
                        role=u'Music By [All Tracks By]',
                        ),
                    ],
                formats=[
                    discograph.models.Format(
                        descriptions=[
                            u'12"',
                            u'33 \\u2153 RPM',
                            ],
                        name=u'Vinyl',
                        quantity=2,
                        ),
                    ],
                genres=[
                    u'Electronic',
                    ],
                identifiers=[
                    discograph.models.Identifier(
                        type_=u'Matrix / Runout',
                        value=u'MPO SK 032 A1 G PHRUPMASTERGENERAL T27 LONDON',
                        ),
                    discograph.models.Identifier(
                        type_=u'Matrix / Runout',
                        value=u'MPO SK 032 B1',
                        ),
                    discograph.models.Identifier(
                        type_=u'Matrix / Runout',
                        value=u'MPO SK 032 C1',
                        ),
                    discograph.models.Identifier(
                        type_=u'Matrix / Runout',
                        value=u'MPO SK 032 D1',
                        ),
                    ],
                labels=[
                    discograph.models.LabelCredit(
                        catalog_number=u'SK032',
                        label=discograph.models.Label(
                            has_been_scraped=False,
                            name=u'Svek',
                            sublabels=[],
                            ),
                        ),
                    ],
                release_date=datetime.datetime(1999, 3, 1, 0, 0),
                status=u'Accepted',
                styles=[
                    u'Deep House',
                    ],
                title=u'Stockholm',
                tracklist=[
                    discograph.models.Track(
                        artists=[],
                        duration=u'4:45',
                        extra_artists=[],
                        position=u'A',
                        title=u'\\xd6stermalm',
                        ),
                    discograph.models.Track(
                        artists=[],
                        duration=u'6:11',
                        extra_artists=[],
                        position=u'B1',
                        title=u'Vasastaden',
                        ),
                    discograph.models.Track(
                        artists=[],
                        duration=u'2:49',
                        extra_artists=[],
                        position=u'B2',
                        title=u'Kungsholmen',
                        ),
                    discograph.models.Track(
                        artists=[],
                        duration=u'5:38',
                        extra_artists=[],
                        position=u'C1',
                        title=u'S\\xf6dermalm',
                        ),
                    discograph.models.Track(
                        artists=[],
                        duration=u'4:52',
                        extra_artists=[],
                        position=u'C2',
                        title=u'Norrmalm',
                        ),
                    discograph.models.Track(
                        artists=[],
                        duration=u'5:16',
                        extra_artists=[],
                        position=u'D',
                        title=u'Gamla Stan',
                        ),
                    ],
                )
            """)
        assert actual == expected

    def test_02(self):
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
        expected = stringtools.normalize(u"""
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
                companies=[
                    discograph.models.CompanyCredit(
                        company=discograph.models.Label(
                            has_been_scraped=False,
                            name=u'Columbia Records',
                            sublabels=[],
                            ),
                        entity_type=10,
                        entity_type_name=u'Manufactured By',
                        ),
                    discograph.models.CompanyCredit(
                        company=discograph.models.Label(
                            has_been_scraped=False,
                            name=u'Columbia Records',
                            sublabels=[],
                            ),
                        entity_type=9,
                        entity_type_name=u'Distributed By',
                        ),
                    ],
                country=u'US',
                data_quality=u'Correct',
                discogs_id=3,
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
                labels=[
                    discograph.models.LabelCredit(
                        catalog_number=u'CK 63628',
                        label=discograph.models.Label(
                            has_been_scraped=False,
                            name=u'Ruffhouse Records',
                            sublabels=[],
                            ),
                        ),
                    ],
                master_id=66526,
                release_date=datetime.datetime(1999, 7, 13, 0, 0),
                status=u'Accepted',
                styles=[
                    u'Techno',
                    u'Tech House',
                    ],
                title=u'Profound Sounds Vol. 1',
                tracklist=[
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=5,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Heiko Laux',
                                    name_variations=[],
                                    ),
                                join=u'&',
                                ),
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=4,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Johannes Heil',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'7:00',
                        extra_artists=[],
                        position=u'1',
                        title=u'Untitled 8',
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                anv=u'K.A.B.',
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=15525,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Karl Axel Bissler',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'5:28',
                        extra_artists=[],
                        position=u'2',
                        title=u'Anjua (Sneaky 3)',
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=7,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Sylk 130',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'5:25',
                        extra_artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=8,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Mood II Swing',
                                    name_variations=[],
                                    ),
                                role=u'Remix',
                                ),
                            ],
                        position=u'3',
                        title=u'When The Funk Hits The Fan (Mood II Swing When The Dub Hits The Fan)',
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=1,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Persuader, The',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'4:27',
                        extra_artists=[],
                        position=u'4',
                        title=u"What's The Time, Mr. Templar",
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=267132,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Care Company (2)',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'5:36',
                        extra_artists=[],
                        position=u'5',
                        title=u'Vol. 2',
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=6981,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Gez Varley',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'3:37',
                        extra_artists=[],
                        position=u'6',
                        title=u'Political Prisoner',
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=11,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'DJ Dozia',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'5:03',
                        extra_artists=[],
                        position=u'7',
                        title=u'Pop Kulture',
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=10702,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u"Nerio's Dubwork",
                                    name_variations=[],
                                    ),
                                join=u'Meets',
                                ),
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=233190,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Kathy Lee',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'5:42',
                        extra_artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=23,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Alex Hi-Fi',
                                    name_variations=[],
                                    ),
                                role=u'Remix',
                                ),
                            ],
                        position=u'8',
                        title=u'K-Mart Shopping (Hi-Fi Mix)',
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=13,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Blaze',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'5:47',
                        extra_artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=14,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Eight Miles High',
                                    name_variations=[],
                                    ),
                                role=u'Remix',
                                ),
                            ],
                        position=u'9',
                        title=u'Lovelee Dae (Eight Miles High Mix)',
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=67226,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Stacey Pullen',
                                    name_variations=[],
                                    ),
                                join=u'Presents',
                                ),
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=7554,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Black Odyssey',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'6:06',
                        extra_artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=67226,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Stacey Pullen',
                                    name_variations=[],
                                    ),
                                role=u'Presenter',
                                ),
                            ],
                        position=u'10',
                        title=u'Sweat',
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=3906,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Christian Smith & John Selway',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'3:16',
                        extra_artists=[],
                        position=u'11',
                        title=u'Silver',
                        ),
                    discograph.models.Track(
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
                                join=u',',
                                ),
                            ],
                        duration=u'2:46',
                        extra_artists=[],
                        position=u'12',
                        title=u'Untitled',
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=19,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Sound Associates',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'3:41',
                        extra_artists=[],
                        position=u'13',
                        title=u'Boom Box',
                        ),
                    discograph.models.Track(
                        artists=[
                            discograph.models.ArtistCredit(
                                artist=discograph.models.Artist(
                                    aliases=[],
                                    discogs_id=20,
                                    has_been_scraped=False,
                                    members=[],
                                    name=u'Percy X',
                                    name_variations=[],
                                    ),
                                join=u',',
                                ),
                            ],
                        duration=u'3:39',
                        extra_artists=[],
                        position=u'14',
                        title=u'Track 2',
                        ),
                    ],
                )
            """)
        assert actual == expected