# -*- coding: utf-8 -*-
import discograph
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        self.client = discograph.connect()

    def tearDown(self):
        self.client.close()

    def test_0(self):
        artist = discograph.library.Artist.objects.get(name='Morris Day')
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=2,
            role_names=role_names,
            )
        nodes, links = grapher.collect_entities_2(role_names=role_names)
        assert nodes == {
            (1, 23446): {'aliases': set(),
                'distance': 2,
                'id': 23446,
                'key': 'artist-23446',
                'links': {
                    'artist-23446-member-of-artist-2065353',
                    'artist-23446-member-of-artist-32550',
                    },
                'missing': 0,
                'name': 'Soulectro Music',
                'size': 0,
                'type': 'artist'},
            (1, 32550): {'aliases': {(1, 2561672)},
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
                'missing': 0,
                'name': 'Time, The',
                'size': 22,
                'type': 'artist'},
            (1, 37806): {'aliases': set(),
                'distance': 2,
                'id': 37806,
                'key': 'artist-37806',
                'links': {
                    'artist-37806-member-of-artist-2561672',
                    'artist-37806-member-of-artist-32550',
                    'artist-37806-member-of-artist-4165408',
                    'artist-37806-member-of-artist-78746',
                    },
                'missing': 0,
                'name': 'Dreamy Records',
                'size': 0,
                'type': 'artist'},
            (1, 53261): {'aliases': {(1, 242702)},
                'distance': 2,
                'id': 53261,
                'key': 'artist-53261',
                'links': {
                    'artist-53261-alias-artist-242702',
                    'artist-53261-member-of-artist-148601',
                    'artist-53261-member-of-artist-2005240',
                    'artist-53261-member-of-artist-2418056',
                    'artist-53261-member-of-artist-3176386',
                    'artist-53261-member-of-artist-32550',
                    },
                'missing': 0,
                'name': 'MECA Records',
                'size': 0,
                'type': 'artist'},
            (1, 55449): {'aliases': set(),
                'distance': 2,
                'id': 55449,
                'key': 'artist-55449',
                'links': {
                    'artist-55449-member-of-artist-121922',
                    'artist-55449-member-of-artist-2065353',
                    'artist-55449-member-of-artist-2561672',
                    'artist-55449-member-of-artist-32550',
                    'artist-55449-member-of-artist-60375',
                    },
                'missing': 0,
                'name': 'Megaeins Verlag GmbH',
                'size': 0,
                'type': 'artist'},
            (1, 100600): {'aliases': set(),
                'distance': 2,
                'id': 100600,
                'key': 'artist-100600',
                'links': {
                    'artist-100600-member-of-artist-2065353',
                    'artist-100600-member-of-artist-2561672',
                    'artist-100600-member-of-artist-32550',
                    },
                'missing': 0,
                'name': 'Poplife Recordings',
                'size': 0,
                'type': 'artist'},
            (1, 113965): {'aliases': set(),
                'distance': 2,
                'id': 113965,
                'key': 'artist-113965',
                'links': {
                    'artist-113965-member-of-artist-148601',
                    'artist-113965-member-of-artist-2005240',
                    'artist-113965-member-of-artist-2065353',
                    'artist-113965-member-of-artist-2418056',
                    'artist-113965-member-of-artist-2561672',
                    'artist-113965-member-of-artist-32550',
                    },
                'missing': 0,
                'name': 'Phatt Pocket Entertainment',
                'size': 0,
                'type': 'artist'},
            (1, 152882): {'aliases': set(),
                'distance': 0,
                'id': 152882,
                'key': 'artist-152882',
                'links': {
                    'artist-152882-member-of-artist-2561672',
                    'artist-152882-member-of-artist-32550',
                    },
                'missing': 0,
                'name': 'Respira Records',
                'size': 0,
                'type': 'artist'},
            (1, 241356): {'aliases': {(1, 55448)},
                'distance': 2,
                'id': 241356,
                'key': 'artist-241356',
                'links': {
                    'artist-241356-member-of-artist-121922',
                    'artist-241356-member-of-artist-1511897',
                    'artist-241356-member-of-artist-2561672',
                    'artist-241356-member-of-artist-32550',
                    'artist-241356-member-of-artist-60375',
                    'artist-55448-alias-artist-241356',
                    },
                'missing': 0,
                'name': 'Not On Label (Robert Wittek Self-released)',
                'size': 0,
                'type': 'artist'},
            (1, 354129): {'aliases': set(),
                'distance': 2,
                'id': 354129,
                'key': 'artist-354129',
                'links': {
                    'artist-354129-member-of-artist-148601',
                    'artist-354129-member-of-artist-2561672',
                    'artist-354129-member-of-artist-32550',
                    },
                'missing': 0,
                'name': 'Freestate Mars',
                'size': 0,
                'type': 'artist'},
            (1, 409502): {'aliases': set(),
                'distance': 2,
                'id': 409502,
                'key': 'artist-409502',
                'links': {
                    'artist-409502-member-of-artist-32550',
                    'artist-409502-member-of-artist-78746',
                    },
                'missing': 0,
                'name': 'Jameson Broadcast, Inc.',
                'size': 0,
                'type': 'artist'},
            (1, 453969): {'aliases': set(),
                'distance': 2,
                'id': 453969,
                'key': 'artist-453969',
                'links': {
                    'artist-453969-member-of-artist-2005240',
                    'artist-453969-member-of-artist-32550',
                    'artist-453969-member-of-artist-78746',
                    },
                'missing': 0,
                'name': 'Jerry Hubbard',
                'size': 0,
                'type': 'artist'},
            (1, 2561672): {'aliases': {(1, 32550)},
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
                'missing': 0,
                'name': 'Original 7ven, The',
                'size': 14,
                'type': 'artist'},
            }

        assert links == {
            'artist-100600-member-of-artist-2065353': {
                'key': 'artist-100600-member-of-artist-2065353',
                'role': 'Member Of',
                'source': ('artist', 100600),
                'target': ('artist', 2065353)},
            'artist-100600-member-of-artist-2561672': {
                'key': 'artist-100600-member-of-artist-2561672',
                'role': 'Member Of',
                'source': ('artist', 100600),
                'target': ('artist', 2561672)},
            'artist-100600-member-of-artist-32550': {
                'key': 'artist-100600-member-of-artist-32550',
                'role': 'Member Of',
                'source': ('artist', 100600),
                'target': ('artist', 32550)},
            'artist-113965-member-of-artist-148601': {
                'key': 'artist-113965-member-of-artist-148601',
                'role': 'Member Of',
                'source': ('artist', 113965),
                'target': ('artist', 148601)},
            'artist-113965-member-of-artist-2005240': {
                'key': 'artist-113965-member-of-artist-2005240',
                'role': 'Member Of',
                'source': ('artist', 113965),
                'target': ('artist', 2005240)},
            'artist-113965-member-of-artist-2065353': {
                'key': 'artist-113965-member-of-artist-2065353',
                'role': 'Member Of',
                'source': ('artist', 113965),
                'target': ('artist', 2065353)},
            'artist-113965-member-of-artist-2418056': {
                'key': 'artist-113965-member-of-artist-2418056',
                'role': 'Member Of',
                'source': ('artist', 113965),
                'target': ('artist', 2418056)},
            'artist-113965-member-of-artist-2561672': {
                'key': 'artist-113965-member-of-artist-2561672',
                'role': 'Member Of',
                'source': ('artist', 113965),
                'target': ('artist', 2561672)},
            'artist-113965-member-of-artist-32550': {
                'key': 'artist-113965-member-of-artist-32550',
                'role': 'Member Of',
                'source': ('artist', 113965),
                'target': ('artist', 32550)},
            'artist-152882-member-of-artist-2561672': {
                'key': 'artist-152882-member-of-artist-2561672',
                'role': 'Member Of',
                'source': ('artist', 152882),
                'target': ('artist', 2561672)},
            'artist-152882-member-of-artist-32550': {
                'key': 'artist-152882-member-of-artist-32550',
                'role': 'Member Of',
                'source': ('artist', 152882),
                'target': ('artist', 32550)},
            'artist-23446-member-of-artist-2065353': {
                'key': 'artist-23446-member-of-artist-2065353',
                'role': 'Member Of',
                'source': ('artist', 23446),
                'target': ('artist', 2065353)},
            'artist-23446-member-of-artist-32550': {
                'key': 'artist-23446-member-of-artist-32550',
                'role': 'Member Of',
                'source': ('artist', 23446),
                'target': ('artist', 32550)},
            'artist-241356-member-of-artist-121922': {
                'key': 'artist-241356-member-of-artist-121922',
                'role': 'Member Of',
                'source': ('artist', 241356),
                'target': ('artist', 121922)},
            'artist-241356-member-of-artist-1511897': {
                'key': 'artist-241356-member-of-artist-1511897',
                'role': 'Member Of',
                'source': ('artist', 241356),
                'target': ('artist', 1511897)},
            'artist-241356-member-of-artist-2561672': {
                'key': 'artist-241356-member-of-artist-2561672',
                'role': 'Member Of',
                'source': ('artist', 241356),
                'target': ('artist', 2561672)},
            'artist-241356-member-of-artist-32550': {
                'key': 'artist-241356-member-of-artist-32550',
                'role': 'Member Of',
                'source': ('artist', 241356),
                'target': ('artist', 32550)},
            'artist-241356-member-of-artist-60375': {
                'key': 'artist-241356-member-of-artist-60375',
                'role': 'Member Of',
                'source': ('artist', 241356),
                'target': ('artist', 60375)},
            'artist-32550-alias-artist-2561672': {
                'key': 'artist-32550-alias-artist-2561672',
                'role': 'Alias',
                'source': ('artist', 32550),
                'target': ('artist', 2561672)},
            'artist-354129-member-of-artist-148601': {
                'key': 'artist-354129-member-of-artist-148601',
                'role': 'Member Of',
                'source': ('artist', 354129),
                'target': ('artist', 148601)},
            'artist-354129-member-of-artist-2561672': {
                'key': 'artist-354129-member-of-artist-2561672',
                'role': 'Member Of',
                'source': ('artist', 354129),
                'target': ('artist', 2561672)},
            'artist-354129-member-of-artist-32550': {
                'key': 'artist-354129-member-of-artist-32550',
                'role': 'Member Of',
                'source': ('artist', 354129),
                'target': ('artist', 32550)},
            'artist-37806-member-of-artist-2561672': {
                'key': 'artist-37806-member-of-artist-2561672',
                'role': 'Member Of',
                'source': ('artist', 37806),
                'target': ('artist', 2561672)},
            'artist-37806-member-of-artist-32550': {
                'key': 'artist-37806-member-of-artist-32550',
                'role': 'Member Of',
                'source': ('artist', 37806),
                'target': ('artist', 32550)},
            'artist-37806-member-of-artist-4165408': {
                'key': 'artist-37806-member-of-artist-4165408',
                'role': 'Member Of',
                'source': ('artist', 37806),
                'target': ('artist', 4165408)},
            'artist-37806-member-of-artist-78746': {
                'key': 'artist-37806-member-of-artist-78746',
                'role': 'Member Of',
                'source': ('artist', 37806),
                'target': ('artist', 78746)},
            'artist-409502-member-of-artist-32550': {
                'key': 'artist-409502-member-of-artist-32550',
                'role': 'Member Of',
                'source': ('artist', 409502),
                'target': ('artist', 32550)},
            'artist-409502-member-of-artist-78746': {
                'key': 'artist-409502-member-of-artist-78746',
                'role': 'Member Of',
                'source': ('artist', 409502),
                'target': ('artist', 78746)},
            'artist-453969-member-of-artist-2005240': {
                'key': 'artist-453969-member-of-artist-2005240',
                'role': 'Member Of',
                'source': ('artist', 453969),
                'target': ('artist', 2005240)},
            'artist-453969-member-of-artist-32550': {
                'key': 'artist-453969-member-of-artist-32550',
                'role': 'Member Of',
                'source': ('artist', 453969),
                'target': ('artist', 32550)},
            'artist-453969-member-of-artist-78746': {
                'key': 'artist-453969-member-of-artist-78746',
                'role': 'Member Of',
                'source': ('artist', 453969),
                'target': ('artist', 78746)},
            'artist-53261-alias-artist-242702': {
                'key': 'artist-53261-alias-artist-242702',
                'role': 'Alias',
                'source': ('artist', 53261),
                'target': ('artist', 242702)},
            'artist-53261-member-of-artist-148601': {
                'key': 'artist-53261-member-of-artist-148601',
                'role': 'Member Of',
                'source': ('artist', 53261),
                'target': ('artist', 148601)},
            'artist-53261-member-of-artist-2005240': {
                'key': 'artist-53261-member-of-artist-2005240',
                'role': 'Member Of',
                'source': ('artist', 53261),
                'target': ('artist', 2005240)},
            'artist-53261-member-of-artist-2418056': {
                'key': 'artist-53261-member-of-artist-2418056',
                'role': 'Member Of',
                'source': ('artist', 53261),
                'target': ('artist', 2418056)},
            'artist-53261-member-of-artist-3176386': {
                'key': 'artist-53261-member-of-artist-3176386',
                'role': 'Member Of',
                'source': ('artist', 53261),
                'target': ('artist', 3176386)},
            'artist-53261-member-of-artist-32550': {
                'key': 'artist-53261-member-of-artist-32550',
                'role': 'Member Of',
                'source': ('artist', 53261),
                'target': ('artist', 32550)},
            'artist-55448-alias-artist-241356': {
                'key': 'artist-55448-alias-artist-241356',
                'role': 'Alias',
                'source': ('artist', 55448),
                'target': ('artist', 241356)},
            'artist-55449-member-of-artist-121922': {
                'key': 'artist-55449-member-of-artist-121922',
                'role': 'Member Of',
                'source': ('artist', 55449),
                'target': ('artist', 121922)},
            'artist-55449-member-of-artist-2065353': {
                'key': 'artist-55449-member-of-artist-2065353',
                'role': 'Member Of',
                'source': ('artist', 55449),
                'target': ('artist', 2065353)},
            'artist-55449-member-of-artist-2561672': {
                'key': 'artist-55449-member-of-artist-2561672',
                'role': 'Member Of',
                'source': ('artist', 55449),
                'target': ('artist', 2561672)},
            'artist-55449-member-of-artist-32550': {
                'key': 'artist-55449-member-of-artist-32550',
                'role': 'Member Of',
                'source': ('artist', 55449),
                'target': ('artist', 32550)},
            'artist-55449-member-of-artist-60375': {
                'key': 'artist-55449-member-of-artist-60375',
                'role': 'Member Of',
                'source': ('artist', 55449),
                'target': ('artist', 60375)},
            }

    def test_1(self):
        artist = discograph.library.Artist.objects.get(name='Morris Day')
        grapher = discograph.RelationGrapher
        role_names = ['Alias', 'Member Of']
        neighborhood = grapher.get_neighborhood(artist, role_names=role_names)
        assert neighborhood == {
            'aliases': (),
            'id': 152882,
            'links': (
                {'role': 'Member Of', 'source': ('artist', 152882), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 152882), 'target': ('artist', 2561672)},
                ),
            'name': 'Morris Day',
            'nodes': (
                ('artist', 32550),
                ('artist', 152882),
                ('artist', 2561672),
                ),
            'size': 0,
            'type': 'artist',
            }

    def test_2(self):
        artist = discograph.library.Artist.objects.get(name='Time, The')
        grapher = discograph.RelationGrapher
        role_names = ['Alias', 'Member Of']
        neighborhood = grapher.get_neighborhood(artist, role_names=role_names)
        assert neighborhood == {
            'aliases': (2561672,),
            'id': 32550,
            'links': (
                {'role': 'Alias', 'source': ('artist', 32550), 'target': ('artist', 2561672)},
                {'role': 'Member Of', 'source': ('artist', 23446), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 37806), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 53261), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 55449), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 100600), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 113965), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 152882), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 241356), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 354129), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 409502), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 453969), 'target': ('artist', 32550)},
                ),
            'name': 'Time, The',
            'nodes': (
                ('artist', 23446),
                ('artist', 32550),
                ('artist', 37806),
                ('artist', 53261),
                ('artist', 55449),
                ('artist', 100600),
                ('artist', 113965),
                ('artist', 152882),
                ('artist', 241356),
                ('artist', 354129),
                ('artist', 409502),
                ('artist', 453969),
                ('artist', 2561672),
                ),
            'size': 11,
            'type': 'artist',
            }

    def test_3(self):
        artist = discograph.library.Artist.objects.get(name='Time, The')
        grapher = discograph.RelationGrapher
        role_names = ['Member Of', 'Alias']
        neighborhood = grapher.get_neighborhood(artist, role_names=role_names)
        assert neighborhood == {
            'aliases': (2561672,),
            'id': 32550,
            'links': (
                {'role': 'Alias', 'source': ('artist', 32550), 'target': ('artist', 2561672)},
                {'role': 'Member Of', 'source': ('artist', 23446), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 37806), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 53261), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 55449), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 100600), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 113965), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 152882), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 241356), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 354129), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 409502), 'target': ('artist', 32550)},
                {'role': 'Member Of', 'source': ('artist', 453969), 'target': ('artist', 32550)},
                ),
            'name': 'Time, The',
            'nodes': (
                ('artist', 23446),
                ('artist', 32550),
                ('artist', 37806),
                ('artist', 53261),
                ('artist', 55449),
                ('artist', 100600),
                ('artist', 113965),
                ('artist', 152882),
                ('artist', 241356),
                ('artist', 354129),
                ('artist', 409502),
                ('artist', 453969),
                ('artist', 2561672),
                ),
            'size': 11,
            'type': 'artist',
            }

    def test_4(self):
        artist = discograph.library.Artist.objects.get(name='Morris Day')
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            [artist],
            degree=2,
            role_names=role_names,
            )
        network = grapher.get_network()
        assert network == {
            'center': ('artist-152882',),
            'links': (
                {'key': 'artist-23446-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-23446', 'target': 'artist-32550'},
                {'key': 'artist-32550-alias-artist-2561672', 'role': 'Alias', 'source': 'artist-32550', 'target': 'artist-2561672'},
                {'key': 'artist-37806-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-37806', 'target': 'artist-32550'},
                {'key': 'artist-37806-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-37806', 'target': 'artist-2561672'},
                {'key': 'artist-53261-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-53261', 'target': 'artist-32550'},
                {'key': 'artist-55449-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-55449', 'target': 'artist-32550'},
                {'key': 'artist-55449-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-55449', 'target': 'artist-2561672'},
                {'key': 'artist-100600-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-100600', 'target': 'artist-32550'},
                {'key': 'artist-100600-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-100600', 'target': 'artist-2561672'},
                {'key': 'artist-113965-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-113965', 'target': 'artist-32550'},
                {'key': 'artist-113965-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-113965', 'target': 'artist-2561672'},
                {'key': 'artist-152882-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-152882', 'target': 'artist-32550'},
                {'key': 'artist-152882-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-152882', 'target': 'artist-2561672'},
                {'key': 'artist-241356-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-241356', 'target': 'artist-32550'},
                {'key': 'artist-241356-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-241356', 'target': 'artist-2561672'},
                {'key': 'artist-354129-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-354129', 'target': 'artist-32550'},
                {'key': 'artist-354129-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-354129', 'target': 'artist-2561672'},
                {'key': 'artist-409502-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-409502', 'target': 'artist-32550'},
                {'key': 'artist-453969-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-453969', 'target': 'artist-32550'},
                ),
            'nodes': (
                {'distance': 2, 'group': None, 'id': 23446, 'key': 'artist-23446', 'missing': 1, 'name': "Alexander O'Neal", 'size': 0, 'type': 'artist'},
                {'distance': 1, 'group': 1, 'id': 32550, 'key': 'artist-32550', 'missing': 0, 'name': 'Time, The', 'size': 11, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 37806, 'key': 'artist-37806', 'missing': 2, 'name': 'Jesse Johnson', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': 2, 'id': 53261, 'key': 'artist-53261', 'missing': 5, 'name': 'St. Paul', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 55449, 'key': 'artist-55449', 'missing': 3, 'name': 'Terry Lewis', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 100600, 'key': 'artist-100600', 'missing': 1, 'name': 'Monte Moir', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 113965, 'key': 'artist-113965', 'missing': 4, 'name': 'Jellybean Johnson', 'size': 0, 'type': 'artist'},
                {'distance': 0, 'group': None, 'id': 152882, 'key': 'artist-152882', 'missing': 0, 'name': 'Morris Day', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': 3, 'id': 241356, 'key': 'artist-241356', 'missing': 4, 'name': 'James Harris III', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 354129, 'key': 'artist-354129', 'missing': 1, 'name': 'Jerome Benton', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 409502, 'key': 'artist-409502', 'missing': 1, 'name': 'Mark Cardenas', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 453969, 'key': 'artist-453969', 'missing': 2, 'name': 'Jerry Hubbard', 'size': 0, 'type': 'artist'},
                {'distance': 1, 'group': 1, 'id': 2561672, 'key': 'artist-2561672', 'missing': 0, 'name': 'Original 7ven, The', 'size': 7, 'type': 'artist'},
                ),
            }

    def test_5(self):
        artist = discograph.library.Artist.objects.get(name='Morris Day')
        role_names = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            [artist],
            degree=2,
            role_names=role_names,
            )
        network = grapher.get_network()
        assert network == {
            'center': ('artist-152882',),
            'links': (
                {'key': 'artist-23446-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-23446', 'target': 'artist-32550'},
                {'key': 'artist-32550-alias-artist-2561672', 'role': 'Alias', 'source': 'artist-32550', 'target': 'artist-2561672'},
                {'key': 'artist-37806-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-37806', 'target': 'artist-32550'},
                {'key': 'artist-37806-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-37806', 'target': 'artist-2561672'},
                {'key': 'artist-53261-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-53261', 'target': 'artist-32550'},
                {'key': 'artist-55449-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-55449', 'target': 'artist-32550'},
                {'key': 'artist-55449-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-55449', 'target': 'artist-2561672'},
                {'key': 'artist-100600-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-100600', 'target': 'artist-32550'},
                {'key': 'artist-100600-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-100600', 'target': 'artist-2561672'},
                {'key': 'artist-113965-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-113965', 'target': 'artist-32550'},
                {'key': 'artist-113965-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-113965', 'target': 'artist-2561672'},
                {'key': 'artist-152882-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-152882', 'target': 'artist-32550'},
                {'key': 'artist-152882-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-152882', 'target': 'artist-2561672'},
                {'key': 'artist-241356-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-241356', 'target': 'artist-32550'},
                {'key': 'artist-241356-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-241356', 'target': 'artist-2561672'},
                {'key': 'artist-354129-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-354129', 'target': 'artist-32550'},
                {'key': 'artist-354129-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-354129', 'target': 'artist-2561672'},
                {'key': 'artist-409502-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-409502', 'target': 'artist-32550'},
                {'key': 'artist-453969-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-453969', 'target': 'artist-32550'},
                ),
            'nodes': (
                {'distance': 2, 'group': None, 'id': 23446, 'key': 'artist-23446', 'missing': 1, 'name': "Alexander O'Neal", 'size': 0, 'type': 'artist'},
                {'distance': 1, 'group': 1, 'id': 32550, 'key': 'artist-32550', 'missing': 0, 'name': 'Time, The', 'size': 11, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 37806, 'key': 'artist-37806', 'missing': 2, 'name': 'Jesse Johnson', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': 2, 'id': 53261, 'key': 'artist-53261', 'missing': 5, 'name': 'St. Paul', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 55449, 'key': 'artist-55449', 'missing': 3, 'name': 'Terry Lewis', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 100600, 'key': 'artist-100600', 'missing': 1, 'name': 'Monte Moir', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 113965, 'key': 'artist-113965', 'missing': 4, 'name': 'Jellybean Johnson', 'size': 0, 'type': 'artist'},
                {'distance': 0, 'group': None, 'id': 152882, 'key': 'artist-152882', 'missing': 0, 'name': 'Morris Day', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': 3, 'id': 241356, 'key': 'artist-241356', 'missing': 4, 'name': 'James Harris III', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 354129, 'key': 'artist-354129', 'missing': 1, 'name': 'Jerome Benton', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 409502, 'key': 'artist-409502', 'missing': 1, 'name': 'Mark Cardenas', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 453969, 'key': 'artist-453969', 'missing': 2, 'name': 'Jerry Hubbard', 'size': 0, 'type': 'artist'},
                {'distance': 1, 'group': 1, 'id': 2561672, 'key': 'artist-2561672', 'missing': 0, 'name': 'Original 7ven, The', 'size': 7, 'type': 'artist'},
                ),
            }