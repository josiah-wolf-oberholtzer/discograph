# -*- encoding: utf-8 -*-
import discograph
import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = discograph.app.test_client()

    def test_index(self):
        response = self.app.get('/')
        assert response.status == '200 OK'

    def test_artist_200(self):
        response = self.app.get('/artist/32550')
        assert response.status == '200 OK'

    def test_label_404(self):
        response = self.app.get('/label/2')
        assert response.status == '200 OK'

    def test_error(self):
        response = self.app.get('/malformed')
        assert response.status == '404 NOT FOUND'