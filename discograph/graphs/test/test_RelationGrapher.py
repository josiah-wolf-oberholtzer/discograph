import discograph

import unittest


class Test(unittest.TestCase):

    def setUp(self):
        self.client = discograph.connect()

    def tearDown(self):
        self.client.close()

    def test_1(self):
        artist = discograph.models.Artist.objects.get(name='Morris Day')
        grapher = discograph.graphs.RelationGrapher
        neighborhood = grapher.get_neighborhood(artist)
        assert neighborhood == {
            'aliases': (),
            'edges': (
                (152882, 32550, 'Member Of'),
                (152882, 2561672, 'Member Of'),
                ),
            'id': 152882,
            'name': 'Morris Day',
            'nodes': (
                {'id': 32550, 'name': 'Time, The'},
                {'id': 2561672, 'name': 'Original 7ven, The'},
                ),
            'size': 0,
            }

    def test_2(self):
        artist = discograph.models.Artist.objects.get(name='Time, The')
        grapher = discograph.graphs.RelationGrapher
        neighborhood = grapher.get_neighborhood(artist)
        assert neighborhood == {
            'aliases': (2561672,),
            'edges': (
                (23446, 32550, 'Member Of'),
                (32550, 2561672, 'Alias'),
                (37806, 32550, 'Member Of'),
                (53261, 32550, 'Member Of'),
                (55449, 32550, 'Member Of'),
                (100600, 32550, 'Member Of'),
                (113965, 32550, 'Member Of'),
                (152882, 32550, 'Member Of'),
                (241356, 32550, 'Member Of'),
                (354129, 32550, 'Member Of'),
                (409502, 32550, 'Member Of'),
                (453969, 32550, 'Member Of')
                ),
            'id': 32550,
            'name': 'Time, The',
            'nodes': (
                {'id': 23446, 'name': "Alexander O'Neal"},
                {'id': 37806, 'name': 'Jesse Johnson'},
                {'id': 53261, 'name': 'St. Paul'},
                {'id': 55449, 'name': 'Terry Lewis'},
                {'id': 100600, 'name': 'Monte Moir'},
                {'id': 113965, 'name': 'Jellybean Johnson'},
                {'id': 152882, 'name': 'Morris Day'},
                {'id': 241356, 'name': 'James Harris III'},
                {'id': 354129, 'name': 'Jerome Benton'},
                {'id': 409502, 'name': 'Mark Cardenas'},
                {'id': 453969, 'name': 'Jerry Hubbard'},
                {'id': 2561672, 'name': 'Original 7ven, The'},
                ),
            'size': 11,
            }

    def test_3(self):
        artist = discograph.models.Artist.objects.get(name='Morris Day')
        grapher = discograph.graphs.RelationGrapher([artist], 1)
        network = grapher.get_network()
        assert network == {
            'center': [152882],
            'links': (
                {'role': 'Alias', 'source': 32550, 'target': 2561672},
                {'role': 'Member Of', 'source': 152882, 'target': 32550},
                {'role': 'Member Of', 'source': 152882, 'target': 2561672},
                ),
            'nodes': (
                {'distance': 1, 'group': 1, 'id': 32550, 'missing': 10, 'name': 'Time, The', 'size': 11},
                {'distance': 0, 'group': None, 'id': 152882, 'missing': 0, 'name': 'Morris Day', 'size': 0},
                {'distance': 1, 'group': 1, 'id': 2561672, 'missing': 6, 'name': 'Original 7ven, The', 'size': 7},
                ),
            }

    def test_4(self):
        artist = discograph.models.Artist.objects.get(name='Morris Day')
        grapher = discograph.graphs.RelationGrapher([artist], 2)
        network = grapher.get_network()
        assert network == {
            'center': [152882],
            'links': (
                {'role': 'Member Of', 'source': 23446, 'target': 32550},
                {'role': 'Alias', 'source': 32550, 'target': 2561672},
                {'role': 'Member Of', 'source': 37806, 'target': 32550},
                {'role': 'Member Of', 'source': 37806, 'target': 2561672},
                {'role': 'Member Of', 'source': 53261, 'target': 32550},
                {'role': 'Member Of', 'source': 55449, 'target': 32550},
                {'role': 'Member Of', 'source': 55449, 'target': 2561672},
                {'role': 'Member Of', 'source': 100600, 'target': 32550},
                {'role': 'Member Of', 'source': 100600, 'target': 2561672},
                {'role': 'Member Of', 'source': 113965, 'target': 32550},
                {'role': 'Member Of', 'source': 113965, 'target': 2561672},
                {'role': 'Member Of', 'source': 152882, 'target': 32550},
                {'role': 'Member Of', 'source': 152882, 'target': 2561672},
                {'role': 'Member Of', 'source': 241356, 'target': 32550},
                {'role': 'Member Of', 'source': 241356, 'target': 2561672},
                {'role': 'Member Of', 'source': 354129, 'target': 32550},
                {'role': 'Member Of', 'source': 354129, 'target': 2561672},
                {'role': 'Member Of', 'source': 409502, 'target': 32550},
                {'role': 'Member Of', 'source': 453969, 'target': 32550},
                ),
            'nodes': (
                {'distance': 2, 'group': None, 'id': 23446, 'missing': 1, 'name': "Alexander O'Neal", 'size': 0},
                {'distance': 1, 'group': 1, 'id': 32550, 'missing': 0, 'name': 'Time, The', 'size': 11},
                {'distance': 2, 'group': None, 'id': 37806, 'missing': 2, 'name': 'Jesse Johnson', 'size': 0},
                {'distance': 2, 'group': 2, 'id': 53261, 'missing': 5, 'name': 'St. Paul', 'size': 0},
                {'distance': 2, 'group': None, 'id': 55449, 'missing': 3, 'name': 'Terry Lewis', 'size': 0},
                {'distance': 2, 'group': None, 'id': 100600, 'missing': 1, 'name': 'Monte Moir', 'size': 0},
                {'distance': 2, 'group': None, 'id': 113965, 'missing': 4, 'name': 'Jellybean Johnson', 'size': 0},
                {'distance': 0, 'group': None, 'id': 152882, 'missing': 0, 'name': 'Morris Day', 'size': 0},
                {'distance': 2, 'group': 3, 'id': 241356, 'missing': 4, 'name': 'James Harris III', 'size': 0},
                {'distance': 2, 'group': None, 'id': 354129, 'missing': 1, 'name': 'Jerome Benton', 'size': 0},
                {'distance': 2, 'group': None, 'id': 409502, 'missing': 1, 'name': 'Mark Cardenas', 'size': 0},
                {'distance': 2, 'group': None, 'id': 453969, 'missing': 2, 'name': 'Jerry Hubbard', 'size': 0},
                {'distance': 1, 'group': 1, 'id': 2561672, 'missing': 0, 'name': 'Original 7ven, The', 'size': 7},
                ),
            }

    def test_5(self):
        artist = discograph.models.Artist.objects.get(name='Morris Day')
        grapher = discograph.graphs.RelationGrapher(
            [artist], degree=3, max_nodes=5)
        network = grapher.get_network()
        assert network == {
            'center': [152882],
            'links': (
                {'role': 'Alias', 'source': 32550, 'target': 2561672},
                {'role': 'Member Of', 'source': 55449, 'target': 32550},
                {'role': 'Member Of', 'source': 55449, 'target': 2561672},
                {'role': 'Member Of', 'source': 152882, 'target': 32550},
                {'role': 'Member Of', 'source': 152882, 'target': 2561672},
                {'role': 'Member Of', 'source': 409502, 'target': 32550},
                ),
            'nodes': (
                {'distance': 1, 'group': 1, 'id': 32550, 'missing': 8, 'name': 'Time, The', 'size': 11},
                {'distance': 2, 'group': None, 'id': 55449, 'missing': 3, 'name': 'Terry Lewis', 'size': 0},
                {'distance': 0, 'group': None, 'id': 152882, 'missing': 0, 'name': 'Morris Day', 'size': 0},
                {'distance': 2, 'group': None, 'id': 409502, 'missing': 1, 'name': 'Mark Cardenas', 'size': 0},
                {'distance': 1, 'group': 1, 'id': 2561672, 'missing': 5, 'name': 'Original 7ven, The', 'size': 7},
                ),
            }

    def test_6(self):
        artist = discograph.models.Artist.objects.get(discogs_id=289473)
        grapher = discograph.graphs.RelationGrapher(
            [artist], degree=12, max_nodes=100)
        network = grapher.get_network()
        assert network == {}