import discograph
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        discograph.connect()

    def test_1(self):
        artist = discograph.models.Artist.objects.get(name='Morris Day')
        grapher = discograph.graphs.ArtistMembershipGrapher([artist], 3)
        json_data = grapher.to_json()
        assert json_data['nodes'] == [
            {'distance': 3, 'group': None, 'id': 3176386, 'name': 'Minneapolis Allstars, The', 'size': 5},
            {'distance': 3, 'group': None, 'id': 2418056, 'name': 'fDeluxe', 'size': 4},
            {'distance': 3, 'group': None, 'id': 2065353, 'name': 'Flyte Tyme', 'size': 6},
            {'distance': 2, 'group': 3, 'id': 241356, 'name': 'James Harris III', 'size': 0},
            {'distance': 2, 'group': 2, 'id': 53261, 'name': 'St. Paul', 'size': 0},
            {'distance': 2, 'group': 2, 'id': 242702, 'name': 'Paul Peterson', 'size': 0},
            {'distance': 2, 'group': None, 'id': 55449, 'name': 'Terry Lewis', 'size': 0},
            {'distance': 2, 'group': None, 'id': 453969, 'name': 'Jerry Hubbard', 'size': 0},
            {'distance': 2, 'group': None, 'id': 23446, 'name': "Alexander O'Neal", 'size': 0},
            {'distance': 3, 'group': None, 'id': 60375, 'name': 'Jimmy Jam & Terry Lewis', 'size': 2},
            {'distance': 2, 'group': 3, 'id': 55448, 'name': 'Jimmy Jam', 'size': 0},
            {'distance': 3, 'group': None, 'id': 1511897, 'name': 'Mind & Matter', 'size': 1},
            {'distance': 3, 'group': None, 'id': 78746, 'name': "Jesse Johnson's Revue", 'size': 7},
            {'distance': 2, 'group': None, 'id': 100600, 'name': 'Monte Moir', 'size': 0},
            {'distance': 2, 'group': None, 'id': 409502, 'name': 'Mark Cardenas', 'size': 0},
            {'distance': 3, 'group': None, 'id': 4165408, 'name': 'The Vanguard (3)', 'size': 6},
            {'distance': 3, 'group': None, 'id': 121922, 'name': 'J-Beat', 'size': 3},
            {'distance': 1, 'group': 1, 'id': 32550, 'name': 'Time, The', 'size': 11},
            {'distance': 2, 'group': None, 'id': 354129, 'name': 'Jerome Benton', 'size': 0},
            {'distance': 2, 'group': None, 'id': 113965, 'name': 'Jellybean Johnson', 'size': 0},
            {'distance': 2, 'group': None, 'id': 37806, 'name': 'Jesse Johnson', 'size': 0},
            {'distance': 1, 'group': 1, 'id': 2561672, 'name': 'Original 7ven, The', 'size': 7},
            {'distance': 0, 'group': None, 'id': 152882, 'name': 'Morris Day', 'size': 0},
            {'distance': 3, 'group': None, 'id': 2005240, 'name': 'Truth, The (14)', 'size': 8},
            {'distance': 3, 'group': None, 'id': 148601, 'name': 'Family, The (2)', 'size': 5},
            ]
        assert json_data['links'] == [
            {'dotted': False, 'source': 32550, 'target': 23446},
            {'dotted': False, 'source': 2065353, 'target': 23446},
            {'dotted': True, 'source': 2561672, 'target': 32550},
            {'dotted': False, 'source': 32550, 'target': 37806},
            {'dotted': False, 'source': 78746, 'target': 37806},
            {'dotted': False, 'source': 2561672, 'target': 37806},
            {'dotted': False, 'source': 4165408, 'target': 37806},
            {'dotted': False, 'source': 32550, 'target': 53261},
            {'dotted': False, 'source': 148601, 'target': 53261},
            {'dotted': True, 'source': 242702, 'target': 53261},
            {'dotted': False, 'source': 2005240, 'target': 53261},
            {'dotted': False, 'source': 2418056, 'target': 53261},
            {'dotted': False, 'source': 3176386, 'target': 53261},
            {'dotted': True, 'source': 241356, 'target': 55448},
            {'dotted': False, 'source': 32550, 'target': 55449},
            {'dotted': False, 'source': 60375, 'target': 55449},
            {'dotted': False, 'source': 121922, 'target': 55449},
            {'dotted': False, 'source': 2065353, 'target': 55449},
            {'dotted': False, 'source': 2561672, 'target': 55449},
            {'dotted': False, 'source': 32550, 'target': 100600},
            {'dotted': False, 'source': 2065353, 'target': 100600},
            {'dotted': False, 'source': 2561672, 'target': 100600},
            {'dotted': False, 'source': 32550, 'target': 113965},
            {'dotted': False, 'source': 148601, 'target': 113965},
            {'dotted': False, 'source': 2005240, 'target': 113965},
            {'dotted': False, 'source': 2065353, 'target': 113965},
            {'dotted': False, 'source': 2418056, 'target': 113965},
            {'dotted': False, 'source': 2561672, 'target': 113965},
            {'dotted': False, 'source': 32550, 'target': 152882},
            {'dotted': False, 'source': 2561672, 'target': 152882},
            {'dotted': False, 'source': 32550, 'target': 241356},
            {'dotted': False, 'source': 60375, 'target': 241356},
            {'dotted': False, 'source': 121922, 'target': 241356},
            {'dotted': False, 'source': 1511897, 'target': 241356},
            {'dotted': False, 'source': 2561672, 'target': 241356},
            {'dotted': False, 'source': 32550, 'target': 354129},
            {'dotted': False, 'source': 148601, 'target': 354129},
            {'dotted': False, 'source': 2561672, 'target': 354129},
            {'dotted': False, 'source': 32550, 'target': 409502},
            {'dotted': False, 'source': 78746, 'target': 409502},
            {'dotted': False, 'source': 32550, 'target': 453969},
            {'dotted': False, 'source': 78746, 'target': 453969},
            {'dotted': False, 'source': 2005240, 'target': 453969},
            ]

    def test_2(self):
        artist = discograph.models.Artist.objects.get(name='Morris Day')
        grapher = discograph.graphs.ArtistMembershipGrapher([artist], 3)
        json_data = grapher.to_json(max_nodes=10)
        assert json_data['nodes'] == [
            {'distance': 2, 'group': None, 'id': 354129, 'name': 'Jerome Benton', 'size': 0},
            {'distance': 2, 'group': None, 'id': 100600, 'name': 'Monte Moir', 'size': 0},
            {'distance': 0, 'group': None, 'id': 152882, 'name': 'Morris Day', 'size': 0},
            {'distance': 2, 'group': None, 'id': 23446, 'name': "Alexander O'Neal", 'size': 0},
            {'distance': 1, 'group': 1, 'id': 32550, 'name': 'Time, The', 'size': 11},
            {'distance': 2, 'group': None, 'id': 453969, 'name': 'Jerry Hubbard', 'size': 0},
            {'distance': 1, 'group': 1, 'id': 2561672, 'name': 'Original 7ven, The', 'size': 7},
            {'distance': 2, 'group': None, 'id': 55449, 'name': 'Terry Lewis', 'size': 0},
            {'distance': 2, 'group': 2, 'id': 53261, 'name': 'St. Paul', 'size': 0},
            {'distance': 2, 'group': None, 'id': 409502, 'name': 'Mark Cardenas', 'size': 0},
            ]

        assert json_data['links'] == [
            {'dotted': False, 'source': 32550, 'target': 23446},
            {'dotted': True, 'source': 2561672, 'target': 32550},
            {'dotted': False, 'source': 32550, 'target': 53261},
            {'dotted': False, 'source': 32550, 'target': 55449},
            {'dotted': False, 'source': 2561672, 'target': 55449},
            {'dotted': False, 'source': 32550, 'target': 100600},
            {'dotted': False, 'source': 2561672, 'target': 100600},
            {'dotted': False, 'source': 32550, 'target': 152882},
            {'dotted': False, 'source': 2561672, 'target': 152882},
            {'dotted': False, 'source': 32550, 'target': 354129},
            {'dotted': False, 'source': 2561672, 'target': 354129},
            {'dotted': False, 'source': 32550, 'target': 409502},
            {'dotted': False, 'source': 32550, 'target': 453969},
            ]