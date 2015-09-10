# -*- coding: utf-8 -*-
import discograph
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        self.client = discograph.connect()

    def tearDown(self):
        self.client.close()

    def test_1(self):
        artist = discograph.models.Artist.objects.get(name='Morris Day')
        grapher = discograph.RelationGrapher
        neighborhood = grapher.get_neighborhood(artist)
        assert neighborhood == {
            'aliases': (),
            'id': 152882,
            'links': (
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 152882), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 152882), 'target': ('artist', 2561672)},
                {'category': 13, 'release_id': 434800, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 157), 'year': 1992},
                {'category': 13, 'release_id': 568998, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1987},
                {'category': 13, 'release_id': 549122, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1985},
                {'category': 13, 'release_id': 558815, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1988},
                {'category': 13, 'release_id': 683845, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1985},
                {'category': 13, 'release_id': 199762, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1988},
                {'category': 13, 'release_id': 561484, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1985},
                {'category': 13, 'release_id': 319861, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1985},
                {'category': 13, 'release_id': 634789, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1988},
                {'category': 13, 'release_id': 292684, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1987},
                {'category': 13, 'release_id': 632216, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 262918, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1985},
                {'category': 13, 'release_id': 744786, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1988},
                {'category': 13, 'release_id': 616032, 'role': 'Released On', 'source': ('artist', 152882), 'target': ('label', 1000), 'year': 1985},
                ),
            'name': 'Morris Day',
            'nodes': (
                ('artist', 32550),
                ('artist', 152882),
                ('artist', 2561672),
                ('label', 157),
                ('label', 1000),
                ),
            'size': 0,
            'type': 'artist'
            }

    def test_2(self):
        artist = discograph.models.Artist.objects.get(name='Time, The')
        grapher = discograph.RelationGrapher
        neighborhood = grapher.get_neighborhood(artist)
        assert neighborhood == {
            'aliases': (2561672,),
            'id': 32550,
            'links': (
                {'category': 13, 'role': 'Alias', 'source': ('artist', 32550), 'target': ('artist', 2561672)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 23446), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 37806), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 53261), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 55449), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 100600), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 113965), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 152882), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 241356), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 354129), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 409502), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 453969), 'target': ('artist', 32550)},
                {'category': 13, 'release_id': 200218, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 157), 'year': 1990},
                {'category': 13, 'release_id': 173526, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1981},
                {'category': 13, 'release_id': 548462, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1987},
                {'category': 13, 'release_id': 641802, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 450626, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 337143, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1987},
                {'category': 13, 'release_id': 683256, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 576854, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 327754, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1982},
                {'category': 13, 'release_id': 40702, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 313985, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1985},
                {'category': 13, 'release_id': 632323, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1982},
                {'category': 13, 'release_id': 632216, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 625713, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 235614, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 576866, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 573001, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 231562, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1981},
                {'category': 13, 'release_id': 746401, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1981},
                {'category': 13, 'release_id': 587311, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000)},
                {'category': 13, 'release_id': 222815, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1987},
                {'category': 13, 'release_id': 212068, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1987},
                {'category': 13, 'release_id': 203891, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 202809, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1982},
                {'category': 13, 'release_id': 202808, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1984},
                {'category': 13, 'release_id': 200219, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 1000), 'year': 1982},
                {'category': 13, 'release_id': 202801, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 5115), 'year': 1990},
                {'category': 13, 'release_id': 200218, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 5115), 'year': 1990},
                {'category': 13, 'release_id': 363850, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 5115), 'year': 1990},
                {'category': 13, 'release_id': 570937, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 5115), 'year': 1990},
                {'category': 13, 'release_id': 295477, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 5115), 'year': 1990},
                {'category': 13, 'release_id': 292694, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 5115), 'year': 1990},
                {'category': 13, 'release_id': 766798, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 5115), 'year': 1990},
                {'category': 13, 'release_id': 324942, 'role': 'Released On', 'source': ('artist', 32550), 'target': ('label', 29034), 'year': 2004},
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
                ('label', 157),
                ('label', 1000),
                ('label', 5115),
                ('label', 29034),
                ),
            'size': 11,
            'type': 'artist',
            }

    def test_3(self):
        artist = discograph.models.Artist.objects.get(name='Time, The')
        grapher = discograph.RelationGrapher
        role_names = ['Member Of', 'Alias']
        neighborhood = grapher.get_neighborhood(artist, role_names=role_names)
        assert neighborhood == {
            'aliases': (2561672,),
            'id': 32550,
            'links': (
                {'category': 13, 'role': 'Alias', 'source': ('artist', 32550), 'target': ('artist', 2561672)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 23446), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 37806), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 53261), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 55449), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 100600), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 113965), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 152882), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 241356), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 354129), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 409502), 'target': ('artist', 32550)},
                {'category': 13, 'role': 'Member Of', 'source': ('artist', 453969), 'target': ('artist', 32550)},
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
        artist = discograph.models.Artist.objects.get(name='Morris Day')
        grapher = discograph.RelationGrapher(
            [artist], degree=2, role_names=['Alias', 'Member Of'])
        network = grapher.get_network()
        assert network == {
            'center': ('artist-152882',),
            'links': (
                {'category': 13, 'key': 'artist-23446-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-23446', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-32550-alias-artist-2561672', 'role': 'Alias', 'source': 'artist-32550', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-37806-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-37806', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-37806-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-37806', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-53261-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-53261', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-55449-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-55449', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-55449-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-55449', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-100600-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-100600', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-100600-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-100600', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-113965-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-113965', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-113965-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-113965', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-152882-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-152882', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-152882-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-152882', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-241356-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-241356', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-241356-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-241356', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-354129-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-354129', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-354129-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-354129', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-409502-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-409502', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-453969-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-453969', 'target': 'artist-32550'},
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
        artist = discograph.models.Artist.objects.get(name='Morris Day')
        grapher = discograph.RelationGrapher([artist], degree=2)
        network = grapher.get_network()
        assert network == {
            'center': ('artist-152882',),
            'links': (
                {'category': 13, 'key': 'artist-23446-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-23446', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-32550-alias-artist-2561672', 'role': 'Alias', 'source': 'artist-32550', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-32550-released-on-label-157', 'release_id': 200218, 'role': 'Released On', 'source': 'artist-32550', 'target': 'label-157', 'year': 1990},
                {'category': 13, 'key': 'artist-32550-released-on-label-1000', 'release_id': 200219, 'role': 'Released On', 'source': 'artist-32550', 'target': 'label-1000', 'year': 1982},
                {'category': 13, 'key': 'artist-32550-released-on-label-5115', 'release_id': 766798, 'role': 'Released On', 'source': 'artist-32550', 'target': 'label-5115', 'year': 1990},
                {'category': 13, 'key': 'artist-32550-released-on-label-29034', 'release_id': 324942, 'role': 'Released On', 'source': 'artist-32550', 'target': 'label-29034', 'year': 2004},
                {'category': 13, 'key': 'artist-37806-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-37806', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-37806-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-37806', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-53261-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-53261', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-55449-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-55449', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-55449-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-55449', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-100600-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-100600', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-100600-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-100600', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-113965-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-113965', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-113965-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-113965', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-152882-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-152882', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-152882-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-152882', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-152882-released-on-label-157', 'release_id': 434800, 'role': 'Released On', 'source': 'artist-152882', 'target': 'label-157', 'year': 1992},
                {'category': 13, 'key': 'artist-152882-released-on-label-1000', 'release_id': 616032, 'role': 'Released On', 'source': 'artist-152882', 'target': 'label-1000', 'year': 1985},
                {'category': 13, 'key': 'artist-241356-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-241356', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-241356-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-241356', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-354129-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-354129', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-354129-member-of-artist-2561672', 'role': 'Member Of', 'source': 'artist-354129', 'target': 'artist-2561672'},
                {'category': 13, 'key': 'artist-409502-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-409502', 'target': 'artist-32550'},
                {'category': 13, 'key': 'artist-453969-member-of-artist-32550', 'role': 'Member Of', 'source': 'artist-453969', 'target': 'artist-32550'},
                ),
            'nodes': (
                {'distance': 2, 'group': None, 'id': 23446, 'key': 'artist-23446', 'missing': 96, 'name': "Alexander O'Neal", 'size': 0, 'type': 'artist'},
                {'distance': 1, 'group': 1, 'id': 32550, 'key': 'artist-32550', 'missing': 0, 'name': 'Time, The', 'size': 11, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 37806, 'key': 'artist-37806', 'missing': 16, 'name': 'Jesse Johnson', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': 2, 'id': 53261, 'key': 'artist-53261', 'missing': 14, 'name': 'St. Paul', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 55449, 'key': 'artist-55449', 'missing': 3, 'name': 'Terry Lewis', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 100600, 'key': 'artist-100600', 'missing': 1, 'name': 'Monte Moir', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 113965, 'key': 'artist-113965', 'missing': 4, 'name': 'Jellybean Johnson', 'size': 0, 'type': 'artist'},
                {'distance': 0, 'group': None, 'id': 152882, 'key': 'artist-152882', 'missing': 0, 'name': 'Morris Day', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': 3, 'id': 241356, 'key': 'artist-241356', 'missing': 4, 'name': 'James Harris III', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 354129, 'key': 'artist-354129', 'missing': 1, 'name': 'Jerome Benton', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 409502, 'key': 'artist-409502', 'missing': 1, 'name': 'Mark Cardenas', 'size': 0, 'type': 'artist'},
                {'distance': 2, 'group': None, 'id': 453969, 'key': 'artist-453969', 'missing': 2, 'name': 'Jerry Hubbard', 'size': 0, 'type': 'artist'},
                {'distance': 1, 'group': 1, 'id': 2561672, 'key': 'artist-2561672', 'missing': 0, 'name': 'Original 7ven, The', 'size': 7, 'type': 'artist'},
                {'distance': 1, 'group': None, 'id': 157, 'key': 'label-157', 'missing': 0, 'name': 'Reprise Records', 'size': 10, 'type': 'label'},
                {'distance': 1, 'group': None, 'id': 1000, 'key': 'label-1000', 'missing': 0, 'name': 'Warner Bros. Records', 'size': 45, 'type': 'label'},
                {'distance': 2, 'group': None, 'id': 5115, 'key': 'label-5115', 'missing': 0, 'name': 'Paisley Park', 'size': 0, 'type': 'label'},
                {'distance': 2, 'group': None, 'id': 29034, 'key': 'label-29034', 'missing': 0, 'name': 'Pie Records', 'size': 0, 'type': 'label'},
                ),
            }