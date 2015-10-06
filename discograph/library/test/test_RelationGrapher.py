# -*- coding: utf-8 -*-
import discograph
import unittest



class Test(unittest.TestCase):
    """
    Problematic networks:

        - 296570: 306 nodes, 13688 links, 5 pages: 149, 4, 4, 4, 158
        - 1946151: unbalanced paging
        - 491160: bifurcated dense alias networks

    """

    def test_collect_entities_01(self):
        artist = discograph.SqliteEntity.get(entity_type=1, name='Morris Day')
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=1,
            role_names=role_names,
            )
        nodes, links = grapher.collect_entities()

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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
                'type': 'artist',
                },
            }

        assert links == {
            'artist-152882-member-of-artist-2561672': {
                'distance': 0,
                'key': 'artist-152882-member-of-artist-2561672',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 152882),
                'target': (1, 2561672),
                },
            'artist-152882-member-of-artist-32550': {
                'distance': 0,
                'key': 'artist-152882-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 152882),
                'target': (1, 32550),
                },
            'artist-32550-alias-artist-2561672': {
                'distance': 1,
                'key': 'artist-32550-alias-artist-2561672',
                'pages': (1,),
                'role': 'Alias',
                'source': (1, 32550),
                'target': (1, 2561672),
                },
            }

    def test_collect_entities_02(self):
        artist = discograph.SqliteEntity.get(entity_type=1, name='Morris Day')
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=2,
            role_names=role_names,
            )
        nodes, links = grapher.collect_entities()

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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
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
                'pages': (1,),
                'type': 'artist'},
            }

        assert links == {
            'artist-100600-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-100600-member-of-artist-2561672',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 100600),
                'target': (1, 2561672)},
            'artist-100600-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-100600-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 100600),
                'target': (1, 32550)},
            'artist-113965-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-113965-member-of-artist-2561672',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 113965),
                'target': (1, 2561672)},
            'artist-113965-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-113965-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 113965),
                'target': (1, 32550)},
            'artist-152882-member-of-artist-2561672': {
                'distance': 0,
                'key': 'artist-152882-member-of-artist-2561672',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 152882),
                'target': (1, 2561672)},
            'artist-152882-member-of-artist-32550': {
                'distance': 0,
                'key': 'artist-152882-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 152882),
                'target': (1, 32550)},
            'artist-23446-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-23446-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 23446),
                'target': (1, 32550)},
            'artist-241356-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-241356-member-of-artist-2561672',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 241356),
                'target': (1, 2561672)},
            'artist-241356-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-241356-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 241356),
                'target': (1, 32550)},
            'artist-32550-alias-artist-2561672': {
                'distance': 1,
                'key': 'artist-32550-alias-artist-2561672',
                'pages': (1,),
                'role': 'Alias',
                'source': (1, 32550),
                'target': (1, 2561672)},
            'artist-354129-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-354129-member-of-artist-2561672',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 354129),
                'target': (1, 2561672)},
            'artist-354129-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-354129-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 354129),
                'target': (1, 32550)},
            'artist-37806-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-37806-member-of-artist-2561672',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 37806),
                'target': (1, 2561672)},
            'artist-37806-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-37806-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 37806),
                'target': (1, 32550)},
            'artist-409502-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-409502-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 409502),
                'target': (1, 32550)},
            'artist-453969-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-453969-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 453969),
                'target': (1, 32550)},
            'artist-53261-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-53261-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 53261),
                'target': (1, 32550)},
            'artist-55449-member-of-artist-2561672': {
                'distance': 1,
                'key': 'artist-55449-member-of-artist-2561672',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 55449),
                'target': (1, 2561672)},
            'artist-55449-member-of-artist-32550': {
                'distance': 1,
                'key': 'artist-55449-member-of-artist-32550',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 55449),
                'target': (1, 32550)},
            }

    def test_collect_entities_03(self):
        artist = discograph.SqliteEntity.get(entity_type=1, entity_id=910459)
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=1,
            role_names=role_names,
            )
        nodes, links = grapher.collect_entities()
        assert nodes == {
            (1, 328670): {
                'aliases': {263345, 7156, 500061, 635045},
                'distance': 1,
                'id': 328670,
                'key': 'artist-328670',
                'links': {'artist-328670-member-of-artist-910459'},
                'members': set(),
                'missing': 14,
                'name': 'Edward Ball',
                'pages': (1,),
                'type': 'artist'},
            (1, 407775): {
                'aliases': set(),
                'distance': 1,
                'id': 407775,
                'key': 'artist-407775',
                'links': {'artist-407775-member-of-artist-910459'},
                'members': set(),
                'missing': 1,
                'name': 'Mira Aroyo',
                'pages': (1,),
                'type': 'artist'},
            (1, 425145): {
                'aliases': set(),
                'distance': 1,
                'id': 425145,
                'key': 'artist-425145',
                'links': {'artist-425145-member-of-artist-910459'},
                'members': set(),
                'missing': 1,
                'name': 'Morgane Lhote',
                'pages': (1,),
                'type': 'artist'},
            # vvv NO NAME
            #(1, 626678): {
            #    'aliases': set(),
            #    'distance': 1,
            #    'id': 626678,
            #    'key': 'artist-626678',
            #    'links': {'artist-626678-member-of-artist-910459'},
            #    'members': set(),
            #    'missing': 0,
            #    'type': 'artist'},
            # ^^^ NO NAME
            (1, 910459): {
                'aliases': set(),
                'distance': 0,
                'id': 910459,
                'key': 'artist-910459',
                'links': {
                    'artist-1047912-member-of-artist-910459',
                    'artist-1047914-member-of-artist-910459',
                    'artist-1294682-member-of-artist-910459',
                    'artist-1538869-member-of-artist-910459',
                    'artist-328670-member-of-artist-910459',
                    'artist-407775-member-of-artist-910459',
                    'artist-425145-member-of-artist-910459',
                    #'artist-626678-member-of-artist-910459',
                    'artist-971316-member-of-artist-910459'},
                'members': {
                    328670,
                    407775,
                    425145,
                    626678,
                    971316,
                    1047912,
                    1047914,
                    1294682,
                    1538869},
                'missing': 0,
                'name': 'Projects, The',
                'pages': (1,),
                'type': 'artist'},
            (1, 971316): {
                'aliases': set(),
                'distance': 1,
                'id': 971316,
                'key': 'artist-971316',
                'links': {'artist-971316-member-of-artist-910459'},
                'members': set(),
                'missing': 4,
                'name': 'Phil Sutton',
                'pages': (1,),
                'type': 'artist'},
            (1, 1047912): {
                'aliases': set(),
                'distance': 1,
                'id': 1047912,
                'key': 'artist-1047912',
                'links': {'artist-1047912-member-of-artist-910459'},
                'members': set(),
                'missing': 0,
                'name': 'Lisa Rosendahl',
                'pages': (1,),
                'type': 'artist'},
            (1, 1047914): {
                'aliases': set(),
                'distance': 1,
                'id': 1047914,
                'key': 'artist-1047914',
                'links': {'artist-1047914-member-of-artist-910459'},
                'members': set(),
                'missing': 3,
                'name': 'Dino Gollnick',
                'pages': (1,),
                'type': 'artist'},
            (1, 1294682): {
                'aliases': {1932},
                'distance': 1,
                'id': 1294682,
                'key': 'artist-1294682',
                'links': {'artist-1294682-member-of-artist-910459'},
                'members': set(),
                'missing': 2,
                'name': "David O'Malley",
                'pages': (1,),
                'type': 'artist'},
            (1, 1538869): {
                'aliases': set(),
                'distance': 1,
                'id': 1538869,
                'key': 'artist-1538869',
                'links': {'artist-1538869-member-of-artist-910459'},
                'members': set(),
                'missing': 1,
                'name': 'Graeme Wilson (2)',
                'pages': (1,),
                'type': 'artist'},
            }

        assert links == {
            'artist-1047912-member-of-artist-910459': {
                'distance': 0,
                'key': 'artist-1047912-member-of-artist-910459',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 1047912),
                'target': (1, 910459)},
            'artist-1047914-member-of-artist-910459': {
                'distance': 0,
                'key': 'artist-1047914-member-of-artist-910459',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 1047914),
                'target': (1, 910459)},
            'artist-1294682-member-of-artist-910459': {
                'distance': 0,
                'key': 'artist-1294682-member-of-artist-910459',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 1294682),
                'target': (1, 910459)},
            'artist-1538869-member-of-artist-910459': {
                'distance': 0,
                'key': 'artist-1538869-member-of-artist-910459',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 1538869),
                'target': (1, 910459)},
            'artist-328670-member-of-artist-910459': {
                'distance': 0,
                'key': 'artist-328670-member-of-artist-910459',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 328670),
                'target': (1, 910459)},
            'artist-407775-member-of-artist-910459': {
                'distance': 0,
                'key': 'artist-407775-member-of-artist-910459',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 407775),
                'target': (1, 910459)},
            'artist-425145-member-of-artist-910459': {
                'distance': 0,
                'key': 'artist-425145-member-of-artist-910459',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 425145),
                'target': (1, 910459)},
            #'artist-626678-member-of-artist-910459': {
            #    'distance': 0,
            #    'key': 'artist-626678-member-of-artist-910459',
            #    'role': 'Member Of',
            #    'source': (1, 626678),
            #    'target': (1, 910459)},
            'artist-971316-member-of-artist-910459': {
                'distance': 0,
                'key': 'artist-971316-member-of-artist-910459',
                'pages': (1,),
                'role': 'Member Of',
                'source': (1, 971316),
                'target': (1, 910459)},
            }

    def test_collect_entities_04(self):
        artist = discograph.SqliteEntity.get(entity_type=1, entity_id=882758)
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=3,
            role_names=role_names,
            max_nodes=100,
            max_links=200,
            )
        nodes, links = grapher.collect_entities()
        assert 100 < len(nodes)
        assert 200 < len(links)
        pages = set()
        for node in nodes.values():
            pages.update(node['pages'])
        assert pages == {1, 2, 3}

    def test_get_network_01(self):
        artist = discograph.SqliteEntity.get(entity_type=1, name='Morris Day')
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=2,
            max_nodes=5,
            role_names=role_names,
            )
        network = grapher.get_network()
        assert network == {}

    def test_get_network_02(self):
        artist = discograph.SqliteEntity.get(entity_type=1, name='Morris Day')
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=2,
            max_links=4,
            role_names=role_names,
            )
        network = grapher.get_network()
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
                    }
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
                    }
                ),
            }

    def test_get_network_03(self):
        artist = discograph.SqliteEntity.get(entity_type=1, name='Morris Day')
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=1,
            role_names=role_names,
            )
        network = grapher.get_network()
        assert network == {
            'center': 'artist-152882',
            'links': (
                {
                    'distance': 1,
                    'key': 'artist-32550-alias-artist-2561672',
                    'pages': (1,),
                    'role': 'Alias',
                    'source': 'artist-32550',
                    'target': 'artist-2561672',
                    },
                {
                    'distance': 0,
                    'key': 'artist-152882-member-of-artist-32550',
                    'pages': (1,),
                    'role': 'Member Of',
                    'source': 'artist-152882',
                    'target': 'artist-32550',
                    },
                {
                    'distance': 0,
                    'key': 'artist-152882-member-of-artist-2561672',
                    'pages': (1,),
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
                    'pages': (1,),
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
                    'pages': (1,),
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
                    'pages': (1,),
                    'size': 7,
                    'type': 'artist',
                    },
                ),
            }