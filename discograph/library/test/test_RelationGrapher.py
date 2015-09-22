# -*- coding: utf-8 -*-
import discograph
import unittest


class Test(unittest.TestCase):

    def test_01(self):
        artist = discograph.SQLArtist.get(name='Morris Day')
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=1,
            role_names=role_names,
            )
        nodes, links = grapher.collect_entities_2()

        assert nodes == {
            (1, 32550): {
                'aliases': {2561672},
                'distance': 1,
                'id': 32550,
                'key': 'artist-32550',
                'links': {
                    'artist-152882-member-of-artist-32550',
                    'artist-32550-alias-artist-2561672',
                    },
                'members': {
                    23446,
                    37806,
                    53261,
                    55449,
                    100600,
                    113965,
                    152882,
                    241356,
                    354129,
                    409502,
                    453969,
                    },
                'missing': 10,
                'name': 'Time, The',
                'type': 'artist',
                },
            (1, 152882): {
                'aliases': set(),
                'distance': 0,
                'id': 152882,
                'key': 'artist-152882',
                'links': {
                    'artist-152882-member-of-artist-2561672',
                    'artist-152882-member-of-artist-32550',
                    },
                'members': set(),
                'missing': 0,
                'name': 'Morris Day',
                'type': 'artist',
                },
            (1, 2561672): {
                'aliases': {32550},
                'distance': 1,
                'id': 2561672,
                'key': 'artist-2561672',
                'links': {
                    'artist-152882-member-of-artist-2561672',
                    'artist-32550-alias-artist-2561672',
                    },
                'members': {
                    37806,
                    55449,
                    100600,
                    113965,
                    152882,
                    241356,
                    354129,
                    },
                'missing': 6,
                'name': 'Original 7ven, The',
                'type': 'artist',
                },
            }

        assert links == {
            'artist-152882-member-of-artist-2561672': {
                'distance': 0,
                'key': 'artist-152882-member-of-artist-2561672',
                'role': 'Member Of',
                'source': (1, 152882),
                'target': (1, 2561672),
                },
            'artist-152882-member-of-artist-32550': {
                'distance': 0,
                'key': 'artist-152882-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 152882),
                'target': (1, 32550),
                },
            'artist-32550-alias-artist-2561672': {
                'distance': 1,
                'key': 'artist-32550-alias-artist-2561672',
                'role': 'Alias',
                'source': (1, 32550),
                'target': (1, 2561672),
                },
            }

    def test_02(self):
        artist = discograph.SQLArtist.get(name='Morris Day')
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=2,
            role_names=role_names,
            )
        nodes, links = grapher.collect_entities_2()

        assert nodes == {
            (1, 23446): {
                'aliases': set(),
                'distance': 2,
                'id': 23446,
                'key': 'artist-23446',
                'links': {
                    'artist-23446-member-of-artist-32550',
                    },
                'missing': 1,
                'name': "Alexander O'Neal",
                'members': set(),
                'type': 'artist'},
            (1, 32550): {
                'aliases': {2561672},
                'distance': 1,
                'id': 32550,
                'key': 'artist-32550',
                'links': {
                    'artist-100600-member-of-artist-32550',
                    'artist-113965-member-of-artist-32550',
                    'artist-152882-member-of-artist-32550',
                    'artist-23446-member-of-artist-32550',
                    'artist-241356-member-of-artist-32550',
                    'artist-32550-alias-artist-2561672',
                    'artist-354129-member-of-artist-32550',
                    'artist-37806-member-of-artist-32550',
                    'artist-409502-member-of-artist-32550',
                    'artist-453969-member-of-artist-32550',
                    'artist-53261-member-of-artist-32550',
                    'artist-55449-member-of-artist-32550',
                    },
                'members': {
                    23446,
                    37806,
                    53261,
                    55449,
                    100600,
                    113965,
                    152882,
                    241356,
                    354129,
                    409502,
                    453969,
                    },
                'missing': 0,
                'name': 'Time, The',
                'type': 'artist'},
            (1, 37806): {
                'aliases': set(),
                'distance': 2,
                'id': 37806,
                'key': 'artist-37806',
                'links': {
                    'artist-37806-member-of-artist-2561672',
                    'artist-37806-member-of-artist-32550',
                    },
                'members': set(),
                'missing': 2,
                'name': 'Jesse Johnson',
                'type': 'artist'},
            (1, 53261): {
                'aliases': {242702},
                'distance': 2,
                'id': 53261,
                'key': 'artist-53261',
                'links': {
                    'artist-53261-member-of-artist-32550',
                    },
                'members': set(),
                'missing': 5,
                'name': 'St. Paul',
                'type': 'artist'},
            (1, 55449): {
                'aliases': set(),
                'distance': 2,
                'id': 55449,
                'key': 'artist-55449',
                'links': {
                    'artist-55449-member-of-artist-2561672',
                    'artist-55449-member-of-artist-32550',
                    },
                'members': set(),
                'missing': 3,
                'name': 'Terry Lewis',
                'type': 'artist'},
            (1, 100600): {
                'aliases': set(),
                'distance': 2,
                'id': 100600,
                'key': 'artist-100600',
                'links': {
                    'artist-100600-member-of-artist-2561672',
                    'artist-100600-member-of-artist-32550',
                    },
                'members': set(),
                'missing': 1,
                'name': 'Monte Moir',
                'type': 'artist'},
            (1, 113965): {
                'aliases': set(),
                'distance': 2,
                'id': 113965,
                'key': 'artist-113965',
                'links': {
                    'artist-113965-member-of-artist-2561672',
                    'artist-113965-member-of-artist-32550',
                    },
                'members': set(),
                'missing': 4,
                'name': 'Jellybean Johnson',
                'type': 'artist'},
            (1, 152882): {
                'aliases': set(),
                'distance': 0,
                'id': 152882,
                'key': 'artist-152882',
                'links': {
                    'artist-152882-member-of-artist-2561672',
                    'artist-152882-member-of-artist-32550',
                    },
                'members': set(),
                'missing': 0,
                'name': 'Morris Day',
                'type': 'artist'},
            (1, 241356): {
                'aliases': {55448},
                'distance': 2,
                'id': 241356,
                'key': 'artist-241356',
                'links': {
                    'artist-241356-member-of-artist-2561672',
                    'artist-241356-member-of-artist-32550',
                    },
                'members': set(),
                'missing': 4,
                'name': 'James Harris III',
                'type': 'artist'},
            (1, 354129): {
                'aliases': set(),
                'distance': 2,
                'id': 354129,
                'key': 'artist-354129',
                'links': {
                    'artist-354129-member-of-artist-2561672',
                    'artist-354129-member-of-artist-32550',
                    },
                'members': set(),
                'missing': 1,
                'name': 'Jerome Benton',
                'type': 'artist'},
            (1, 409502): {
                'aliases': set(),
                'distance': 2,
                'id': 409502,
                'key': 'artist-409502',
                'links': {
                    'artist-409502-member-of-artist-32550',
                    },
                'members': set(),
                'missing': 1,
                'name': 'Mark Cardenas',
                'type': 'artist'},
            (1, 453969): {
                'aliases': set(),
                'distance': 2,
                'id': 453969,
                'key': 'artist-453969',
                'links': {
                    'artist-453969-member-of-artist-32550',
                    },
                'members': set(),
                'missing': 2,
                'name': 'Jerry Hubbard',
                'type': 'artist'},
            (1, 2561672): {
                'aliases': {32550},
                'distance': 1,
                'id': 2561672,
                'key': 'artist-2561672',
                'links': {
                    'artist-100600-member-of-artist-2561672',
                    'artist-113965-member-of-artist-2561672',
                    'artist-152882-member-of-artist-2561672',
                    'artist-241356-member-of-artist-2561672',
                    'artist-32550-alias-artist-2561672',
                    'artist-354129-member-of-artist-2561672',
                    'artist-37806-member-of-artist-2561672',
                    'artist-55449-member-of-artist-2561672',
                    },
                'members': {
                    37806,
                    55449,
                    100600,
                    113965,
                    152882,
                    241356,
                    354129
                    },
                'missing': 0,
                'name': 'Original 7ven, The',
                'type': 'artist'},
            }

        assert links == {
            'artist-100600-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-100600-member-of-artist-2561672',
                'role': 'Member Of',
                'source': (1, 100600),
                'target': (1, 2561672)},
            'artist-100600-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-100600-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 100600),
                'target': (1, 32550)},
            'artist-113965-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-113965-member-of-artist-2561672',
                'role': 'Member Of',
                'source': (1, 113965),
                'target': (1, 2561672)},
            'artist-113965-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-113965-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 113965),
                'target': (1, 32550)},
            'artist-152882-member-of-artist-2561672': {
                'distance': 0,
                'key': 'artist-152882-member-of-artist-2561672',
                'role': 'Member Of',
                'source': (1, 152882),
                'target': (1, 2561672)},
            'artist-152882-member-of-artist-32550': {
                'distance': 0,
                'key': 'artist-152882-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 152882),
                'target': (1, 32550)},
            'artist-23446-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-23446-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 23446),
                'target': (1, 32550)},
            'artist-241356-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-241356-member-of-artist-2561672',
                'role': 'Member Of',
                'source': (1, 241356),
                'target': (1, 2561672)},
            'artist-241356-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-241356-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 241356),
                'target': (1, 32550)},
            'artist-32550-alias-artist-2561672': {
                'distance': 1,
                'key': 'artist-32550-alias-artist-2561672',
                'role': 'Alias',
                'source': (1, 32550),
                'target': (1, 2561672)},
            'artist-354129-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-354129-member-of-artist-2561672',
                'role': 'Member Of',
                'source': (1, 354129),
                'target': (1, 2561672)},
            'artist-354129-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-354129-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 354129),
                'target': (1, 32550)},
            'artist-37806-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-37806-member-of-artist-2561672',
                'role': 'Member Of',
                'source': (1, 37806),
                'target': (1, 2561672)},
            'artist-37806-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-37806-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 37806),
                'target': (1, 32550)},
            'artist-409502-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-409502-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 409502),
                'target': (1, 32550)},
            'artist-453969-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-453969-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 453969),
                'target': (1, 32550)},
            'artist-53261-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-53261-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 53261),
                'target': (1, 32550)},
            'artist-55449-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-55449-member-of-artist-2561672',
                'role': 'Member Of',
                'source': (1, 55449),
                'target': (1, 2561672)},
            'artist-55449-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-55449-member-of-artist-32550',
                'role': 'Member Of',
                'source': (1, 55449),
                'target': (1, 32550)},
            }

    def test_03(self):
        artist = discograph.SQLArtist.get(name='Morris Day')
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=1,
            role_names=role_names,
            )
        network = grapher.get_network_2()

        assert network == {
            'center': 'artist-152882',
            'links': (
                {
                    'distance': 1,
                    'key': 'artist-32550-alias-artist-2561672',
                    'role': 'Alias',
                    'source': 'artist-32550',
                    'target': 'artist-2561672',
                    },
                {
                    'distance': 0,
                    'key': 'artist-152882-member-of-artist-32550',
                    'role': 'Member Of',
                    'source': 'artist-152882',
                    'target': 'artist-32550',
                    },
                {
                    'distance': 0,
                    'key': 'artist-152882-member-of-artist-2561672',
                    'role': 'Member Of',
                    'source': 'artist-152882',
                    'target': 'artist-2561672',
                    },
                ),
            'nodes': (
                {
                    'aliases': (2561672,),
                    'cluster': 1,
                    'distance': 1,
                    'id': 32550,
                    'key': 'artist-32550',
                    'links': (
                        'artist-152882-member-of-artist-32550',
                        'artist-32550-alias-artist-2561672',
                        ),
                    'missing': 10,
                    'name': 'Time, The',
                    'size': 11,
                    'type': 'artist',
                    },
                {
                    'distance': 0,
                    'id': 152882,
                    'key': 'artist-152882',
                    'links': (
                        'artist-152882-member-of-artist-2561672',
                        'artist-152882-member-of-artist-32550',
                        ),
                    'missing': 0,
                    'name': 'Morris Day',
                    'size': 0,
                    'type': 'artist',
                    },
                {
                    'aliases': (32550,),
                    'cluster': 1,
                    'distance': 1,
                    'id': 2561672,
                    'key': 'artist-2561672',
                    'links': (
                        'artist-152882-member-of-artist-2561672',
                        'artist-32550-alias-artist-2561672',
                        ),
                    'missing': 6,
                    'name': 'Original 7ven, The',
                    'size': 7,
                    'type': 'artist',
                    },
                ),
            }

    def test_04(self):
        artist = discograph.SQLArtist.get(id=910459)
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=1,
            role_names=role_names,
            )
        nodes, links = grapher.collect_entities_2()