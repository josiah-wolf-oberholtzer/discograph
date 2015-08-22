import datetime
import unittest
from discograph import models


class Test(unittest.TestCase):

    def test_1(self):
        date_string = '1989-06-23'
        date = models.Release.parse_release_date(date_string)
        assert date == datetime.datetime(1989, 6, 23)

    def test_2(self):
        date_string = '2015-06-31'
        date = models.Release.parse_release_date(date_string)
        assert date == datetime.datetime(2015, 7, 1)

    def test_3(self):
        date_string = '2014-06-00'
        date = models.Release.parse_release_date(date_string)
        assert date == datetime.datetime(2014, 6, 1)

    def test_4(self):
        date_string = '2013-00-00'
        date = models.Release.parse_release_date(date_string)
        assert date == datetime.datetime(2013, 1, 1)

    def test_5(self):
        date_string = '2001'
        date = models.Release.parse_release_date(date_string)
        assert date == datetime.datetime(2001, 1, 1, 0, 0)

    def test_6(self):
        date_string = '1971'
        date = models.Release.parse_release_date(date_string)
        assert date == datetime.datetime(1971, 1, 1, 0, 0)

    def test_7(self):
        date_string = '?'
        date = models.Release.parse_release_date(date_string)
        assert date is None

    def test_8(self):
        date_string = '????'
        date = models.Release.parse_release_date(date_string)
        assert date is None

    def test_9(self):
        date_string = 'None'
        date = models.Release.parse_release_date(date_string)
        assert date is None

    def test_10(self):
        date_string = ''
        date = models.Release.parse_release_date(date_string)
        assert date is None

    def test_11(self):
        date_string = ''
        date = models.Release.parse_release_date(date_string)
        assert date is None