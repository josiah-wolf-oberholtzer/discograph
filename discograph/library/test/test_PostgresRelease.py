# -*- encoding: utf-8 -*-
import discograph
import unittest
from abjad import stringtools
from discograph.library.Bootstrapper import Bootstrapper


class Test(unittest.TestCase):

    def test_01(self):
        iterator = Bootstrapper.get_iterator('release')
        release_element = next(iterator)
        release = discograph.PostgresRelease.from_element(release_element)
        actual = format(release)
        expected = stringtools.normalize(u"""
            discograph.library.PostgresRelease(
                artists=[
                    {
                        'id': 1,
                        'join': ',',
                        'name': 'The Persuader',
                        },
                    ],
                companies=[
                    {
                        'entity_type': 23,
                        'entity_type_name': 'Recorded At',
                        'id': 271046,
                        'name': 'The Globe Studios',
                        },
                    {
                        'entity_type': 17,
                        'entity_type_name': 'Pressed By',
                        'id': 56025,
                        'name': 'MPO',
                        },
                    ],
                country='Sweden',
                extra_artists=[
                    {
                        'id': 239,
                        'name': 'Jesper Dahlbäck',
                        'roles': [
                            {
                                'detail': 'All Tracks By',
                                'name': 'Music By',
                                },
                            ],
                        },
                    ],
                formats=[
                    {
                        'descriptions': ['12"', '33 ⅓ RPM'],
                        'name': 'Vinyl',
                        'quantity': '2',
                        },
                    ],
                genres=['Electronic'],
                id=1,
                identifiers=[
                    {
                        'description': 'A-Side',
                        'type': 'Matrix / Runout',
                        'value': 'MPO SK 032 A1 G PHRUPMASTERGENERAL T27 LONDON',
                        },
                    {
                        'description': 'B-Side',
                        'type': 'Matrix / Runout',
                        'value': 'MPO SK 032 B1',
                        },
                    {
                        'description': 'C-Side',
                        'type': 'Matrix / Runout',
                        'value': 'MPO SK 032 C1',
                        },
                    {
                        'description': 'D-Side',
                        'type': 'Matrix / Runout',
                        'value': 'MPO SK 032 D1',
                        },
                    ],
                labels=[
                    {
                        'catalog_number': 'SK032',
                        'name': 'Svek',
                        },
                    ],
                release_date=datetime.datetime(1999, 3, 1, 0, 0),
                styles=['Deep House'],
                title='Stockholm',
                tracklist=[
                    {
                        'duration': '4:45',
                        'position': 'A',
                        'title': 'Östermalm',
                        },
                    {
                        'duration': '6:11',
                        'position': 'B1',
                        'title': 'Vasastaden',
                        },
                    {
                        'duration': '2:49',
                        'position': 'B2',
                        'title': 'Kungsholmen',
                        },
                    {
                        'duration': '5:38',
                        'position': 'C1',
                        'title': 'Södermalm',
                        },
                    {
                        'duration': '4:52',
                        'position': 'C2',
                        'title': 'Norrmalm',
                        },
                    {
                        'duration': '5:16',
                        'position': 'D',
                        'title': 'Gamla Stan',
                        },
                    ],
                )
            """)
        assert actual == expected

    def test_02(self):
        iterator = Bootstrapper.get_iterator('release')
        release_element = next(iterator)
        release_element = next(iterator)
        release_element = next(iterator)
        release = discograph.PostgresRelease.from_element(release_element)
        actual = format(release)
        expected = stringtools.normalize(r'''
            discograph.library.PostgresRelease(
                artists=[
                    {
                        'id': 3,
                        'name': 'Josh Wink',
                        },
                    ],
                companies=[
                    {
                        'entity_type': 10,
                        'entity_type_name': 'Manufactured By',
                        'id': 93330,
                        'name': 'Columbia Records',
                        },
                    {
                        'entity_type': 9,
                        'entity_type_name': 'Distributed By',
                        'id': 93330,
                        'name': 'Columbia Records',
                        },
                    ],
                country='US',
                extra_artists=[
                    {
                        'id': 3,
                        'name': 'Josh Wink',
                        'roles': [
                            {
                                'name': 'DJ Mix',
                                },
                            ],
                        },
                    ],
                formats=[
                    {
                        'descriptions': ['Compilation', 'Mixed'],
                        'name': 'CD',
                        'quantity': '1',
                        },
                    ],
                genres=['Electronic'],
                id=3,
                identifiers=[
                    {
                        'description': None,
                        'type': 'Barcode',
                        'value': '074646362822',
                        },
                    ],
                labels=[
                    {
                        'catalog_number': 'CK 63628',
                        'name': 'Ruffhouse Records',
                        },
                    ],
                master_id=66526,
                release_date=datetime.datetime(1999, 7, 13, 0, 0),
                styles=['Techno', 'Tech House'],
                title='Profound Sounds Vol. 1',
                tracklist=[
                    {
                        'artists': [
                            {
                                'id': 5,
                                'join': '&',
                                'name': 'Heiko Laux',
                                },
                            {
                                'id': 4,
                                'join': ',',
                                'name': 'Johannes Heil',
                                },
                            ],
                        'duration': '7:00',
                        'position': '1',
                        'title': 'Untitled 8',
                        },
                    {
                        'artists': [
                            {
                                'anv': 'K.A.B.',
                                'id': 15525,
                                'join': ',',
                                'name': 'Karl Axel Bissler',
                                },
                            ],
                        'duration': '5:28',
                        'position': '2',
                        'title': 'Anjua (Sneaky 3)',
                        },
                    {
                        'artists': [
                            {
                                'id': 7,
                                'join': ',',
                                'name': 'Sylk 130',
                                },
                            ],
                        'duration': '5:25',
                        'extra_artists': [
                            {
                                'id': 8,
                                'name': 'Mood II Swing',
                                'roles': [
                                    {
                                        'name': 'Remix',
                                        },
                                    ],
                                },
                            ],
                        'position': '3',
                        'title': 'When The Funk Hits The Fan (Mood II Swing When The Dub Hits The Fan)',
                        },
                    {
                        'artists': [
                            {
                                'id': 1,
                                'join': ',',
                                'name': 'The Persuader',
                                },
                            ],
                        'duration': '4:27',
                        'position': '4',
                        'title': "What's The Time, Mr. Templar",
                        },
                    {
                        'artists': [
                            {
                                'id': 267132,
                                'join': ',',
                                'name': 'Care Company (2)',
                                },
                            ],
                        'duration': '5:36',
                        'position': '5',
                        'title': 'Vol. 2',
                        },
                    {
                        'artists': [
                            {
                                'id': 6981,
                                'join': ',',
                                'name': 'Gez Varley',
                                },
                            ],
                        'duration': '3:37',
                        'position': '6',
                        'title': 'Political Prisoner',
                        },
                    {
                        'artists': [
                            {
                                'id': 11,
                                'join': ',',
                                'name': 'DJ Dozia',
                                },
                            ],
                        'duration': '5:03',
                        'position': '7',
                        'title': 'Pop Kulture',
                        },
                    {
                        'artists': [
                            {
                                'id': 10702,
                                'join': 'Meets',
                                'name': "Nerio's Dubwork",
                                },
                            {
                                'id': 233190,
                                'join': ',',
                                'name': 'Kathy Lee',
                                },
                            ],
                        'duration': '5:42',
                        'extra_artists': [
                            {
                                'id': 23,
                                'name': 'Alex Hi-Fi',
                                'roles': [
                                    {
                                        'name': 'Remix',
                                        },
                                    ],
                                },
                            ],
                        'position': '8',
                        'title': 'K-Mart Shopping (Hi-Fi Mix)',
                        },
                    {
                        'artists': [
                            {
                                'id': 13,
                                'join': ',',
                                'name': 'Blaze',
                                },
                            ],
                        'duration': '5:47',
                        'extra_artists': [
                            {
                                'id': 14,
                                'name': 'Eight Miles High',
                                'roles': [
                                    {
                                        'name': 'Remix',
                                        },
                                    ],
                                },
                            ],
                        'position': '9',
                        'title': 'Lovelee Dae (Eight Miles High Mix)',
                        },
                    {
                        'artists': [
                            {
                                'id': 67226,
                                'join': 'Presents',
                                'name': 'Stacey Pullen',
                                },
                            {
                                'id': 7554,
                                'join': ',',
                                'name': 'Black Odyssey',
                                },
                            ],
                        'duration': '6:06',
                        'extra_artists': [
                            {
                                'id': 67226,
                                'name': 'Stacey Pullen',
                                'roles': [
                                    {
                                        'name': 'Presenter',
                                        },
                                    ],
                                },
                            ],
                        'position': '10',
                        'title': 'Sweat',
                        },
                    {
                        'artists': [
                            {
                                'id': 3906,
                                'join': ',',
                                'name': 'Christian Smith & John Selway',
                                },
                            ],
                        'duration': '3:16',
                        'position': '11',
                        'title': 'Silver',
                        },
                    {
                        'artists': [
                            {
                                'id': 3,
                                'join': ',',
                                'name': 'Josh Wink',
                                },
                            ],
                        'duration': '2:46',
                        'position': '12',
                        'title': 'Untitled',
                        },
                    {
                        'artists': [
                            {
                                'id': 19,
                                'join': ',',
                                'name': 'Sound Associates',
                                },
                            ],
                        'duration': '3:41',
                        'position': '13',
                        'title': 'Boom Box',
                        },
                    {
                        'artists': [
                            {
                                'id': 20,
                                'join': ',',
                                'name': 'Percy X',
                                },
                            ],
                        'duration': '3:39',
                        'position': '14',
                        'title': 'Track 2',
                        },
                    ],
                )
            ''')
        assert actual == expected