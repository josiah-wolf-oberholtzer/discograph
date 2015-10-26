# -*- encoding: utf-8 -*-
import discograph
import json
import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = discograph.app.test_client()

    def test_network_01(self):
        response = self.app.get('/api/artist/network/32550')
        assert response.status == '200 OK'

    def test_network_02(self):
        response = self.app.get('/api/artist/network/999999999999')
        assert response.status == '400 BAD REQUEST'

    def test_network_03(self):
        response = self.app.get('/api/label/network/1')
        assert response.status == '200 OK'

    def test_search_01(self):
        response = self.app.get('/api/search/Morris')
        assert response.status == '200 OK'
        data = json.loads(response.data.decode('utf-8'))
        assert data == {
            'results': [
                {'key': 'artist-175844', 'name': 'Morris'},
                {'key': 'label-501118', 'name': 'Morris'},
                {'key': 'artist-2370760', 'name': 'Morris G. Morris'},
                {'key': 'artist-3723', 'name': 'Chris Morris'},
                {'key': 'artist-3985', 'name': 'Mixmaster Morris'},
                {'key': 'artist-4518', 'name': 'Morris Brown'},
                {'key': 'artist-24763', 'name': 'Morgan Morris'},
                {'key': 'artist-27005', 'name': 'Morris Nightingale'},
                {'key': 'artist-32224', 'name': 'DJ Morris'},
                {'key': 'artist-33751', 'name': 'Max & Morris'},
                ],
            }

    def test_search_02(self):
        response = self.app.get('/api/search/Morris+Day')
        assert response.status == '200 OK'
        data = json.loads(response.data.decode('utf-8'))
        assert data == {
            'results': [
                {'key': 'artist-152882', 'name': 'Morris Day'}
                ],
            }

    def test_timeline_01(self):
        response = self.app.get('/api/artist/timeline/32550')
        assert response.status == '200 OK'