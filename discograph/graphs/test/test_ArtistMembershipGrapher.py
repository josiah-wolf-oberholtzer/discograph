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
            {'distance': 3, 'group': None, 'id': 3176386, 'incomplete': True, 'name': 'Minneapolis Allstars, The', 'size': 5},
            {'distance': 3, 'group': 4, 'id': 2418056, 'incomplete': True, 'name': 'fDeluxe', 'size': 4},
            {'distance': 3, 'group': None, 'id': 2065353, 'incomplete': True, 'name': 'Flyte Tyme', 'size': 6},
            {'distance': 2, 'group': 3, 'id': 241356, 'incomplete': False, 'name': 'James Harris III', 'size': 0},
            {'distance': 2, 'group': 2, 'id': 53261, 'incomplete': False, 'name': 'St. Paul', 'size': 0},
            {'distance': 2, 'group': 2, 'id': 242702, 'incomplete': False, 'name': 'Paul Peterson', 'size': 0},
            {'distance': 2, 'group': None, 'id': 55449, 'incomplete': False, 'name': 'Terry Lewis', 'size': 0},
            {'distance': 2, 'group': None, 'id': 453969, 'incomplete': False, 'name': 'Jerry Hubbard', 'size': 0},
            {'distance': 2, 'group': None, 'id': 23446, 'incomplete': False, 'name': "Alexander O'Neal", 'size': 0},
            {'distance': 3, 'group': 5, 'id': 60375, 'incomplete': False, 'name': 'Jimmy Jam & Terry Lewis', 'size': 2},
            {'distance': 2, 'group': 3, 'id': 55448, 'incomplete': False, 'name': 'Jimmy Jam', 'size': 0},
            {'distance': 3, 'group': None, 'id': 1511897, 'incomplete': False, 'name': 'Mind & Matter', 'size': 1},
            {'distance': 3, 'group': None, 'id': 78746, 'incomplete': True, 'name': "Jesse Johnson's Revue", 'size': 7},
            {'distance': 3, 'group': 5, 'id': 4215643, 'incomplete': False, 'name': 'Flyte Tyme (2)', 'size': 0},
            {'distance': 2, 'group': None, 'id': 100600, 'incomplete': False, 'name': 'Monte Moir', 'size': 0},
            {'distance': 2, 'group': None, 'id': 409502, 'incomplete': False, 'name': 'Mark Cardenas', 'size': 0},
            {'distance': 3, 'group': None, 'id': 4165408, 'incomplete': True, 'name': 'The Vanguard (3)', 'size': 6},
            {'distance': 3, 'group': None, 'id': 121922, 'incomplete': True, 'name': 'J-Beat', 'size': 3},
            {'distance': 1, 'group': 1, 'id': 32550, 'incomplete': False, 'name': 'Time, The', 'size': 11},
            {'distance': 2, 'group': None, 'id': 354129, 'incomplete': False, 'name': 'Jerome Benton', 'size': 0},
            {'distance': 2, 'group': None, 'id': 113965, 'incomplete': False, 'name': 'Jellybean Johnson', 'size': 0},
            {'distance': 2, 'group': None, 'id': 37806, 'incomplete': False, 'name': 'Jesse Johnson', 'size': 0},
            {'distance': 1, 'group': 1, 'id': 2561672, 'incomplete': False, 'name': 'Original 7ven, The', 'size': 7},
            {'distance': 0, 'group': None, 'id': 152882, 'incomplete': False, 'name': 'Morris Day', 'size': 0},
            {'distance': 3, 'group': None, 'id': 2005240, 'incomplete': True, 'name': 'Truth, The (14)', 'size': 8},
            {'distance': 3, 'group': 4, 'id': 148601, 'incomplete': True, 'name': 'Family, The (2)', 'size': 5}
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
            {'dotted': True, 'source': 4215643, 'target': 60375},
            {'dotted': False, 'source': 32550, 'target': 100600},
            {'dotted': False, 'source': 2065353, 'target': 100600},
            {'dotted': False, 'source': 2561672, 'target': 100600},
            {'dotted': False, 'source': 32550, 'target': 113965},
            {'dotted': False, 'source': 148601, 'target': 113965},
            {'dotted': False, 'source': 2005240, 'target': 113965},
            {'dotted': False, 'source': 2065353, 'target': 113965},
            {'dotted': False, 'source': 2418056, 'target': 113965},
            {'dotted': False, 'source': 2561672, 'target': 113965},
            {'dotted': True, 'source': 2418056, 'target': 148601},
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
            {'distance': 2, 'group': None, 'id': 354129, 'incomplete': True, 'name': 'Jerome Benton', 'size': 0},
            {'distance': 2, 'group': None, 'id': 100600, 'incomplete': True, 'name': 'Monte Moir', 'size': 0},
            {'distance': 0, 'group': None, 'id': 152882, 'incomplete': False, 'name': 'Morris Day', 'size': 0},
            {'distance': 2, 'group': None, 'id': 23446, 'incomplete': True, 'name': "Alexander O'Neal", 'size': 0},
            {'distance': 1, 'group': 1, 'id': 32550, 'incomplete': True, 'name': 'Time, The', 'size': 11},
            {'distance': 2, 'group': None, 'id': 453969, 'incomplete': True, 'name': 'Jerry Hubbard', 'size': 0},
            {'distance': 1, 'group': 1, 'id': 2561672, 'incomplete': True, 'name': 'Original 7ven, The', 'size': 7},
            {'distance': 2, 'group': None, 'id': 55449, 'incomplete': True, 'name': 'Terry Lewis', 'size': 0},
            {'distance': 2, 'group': 2, 'id': 53261, 'incomplete': True, 'name': 'St. Paul', 'size': 0},
            {'distance': 2, 'group': None, 'id': 409502, 'incomplete': True, 'name': 'Mark Cardenas', 'size': 0}
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