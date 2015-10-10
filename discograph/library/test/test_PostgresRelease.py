# -*- encoding: utf-8 -*-
import discograph
import unittest
from abjad import stringtools
from discograph.library.Bootstrapper import Bootstrapper


class Test(unittest.TestCase):

    def test_01(self):
        iterator = Bootstrapper.get_iterator('release')
        element = next(iterator)
        release = discograph.PostgresRelease.from_element(element)
        actual = format(release)
        expected = stringtools.normalize(u"""
            discograph.library.postgres.PostgresRelease(
                artists=[
                    {
                        'id': 1,
                        'name': 'Persuader, The',
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
                        'role': 'Music By [All Tracks By]',
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