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
                        },
                    ],
                companies=[
                    {
                        },
                    {
                        },
                    ],
                country='Sweden',
                extra_artists=[
                    {
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
                release_date=datetime.datetime(1999, 3, 1, 0, 0),
                styles=['Deep House'],
                title='Stockholm',
                )
            """)
        assert actual == expected