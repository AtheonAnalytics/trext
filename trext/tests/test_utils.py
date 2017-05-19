from unittest import TestCase
from datetime import date, datetime

from trext.db.utils import format_date, format_datetime


class TestDateFormat(TestCase):
    def setUp(self):
        self.date_to_format = date.today()
        self.datetime_to_fail = datetime.today()

    def test_date_type(self):
        self.assertEqual(type(format_date(self.date_to_format)), tuple)

    def test_date_parts(self):
        y, m, d = format_date(self.date_to_format)
        self.assertEqual(y, self.date_to_format.year)
        self.assertEqual(m, self.date_to_format.month)
        self.assertEqual(d, self.date_to_format.day)

    def test_datetime_failure(self):
        self.assertRaises(ValueError, lambda: format_date(self.datetime_to_fail))


class TestDatetimeFormat(TestCase):
    def setUp(self):
        self.datetime_to_format = datetime.today()
        self.date_to_fail = date.today()

    def test_date_type(self):
        self.assertEqual(type(format_datetime(self.datetime_to_format)), tuple)

    def test_date_parts(self):
        y, m, d, h, mi, s, f = format_datetime(self.datetime_to_format)
        self.assertEqual(y, self.datetime_to_format.year)
        self.assertEqual(m, self.datetime_to_format.month)
        self.assertEqual(d, self.datetime_to_format.day)
        self.assertEqual(h, self.datetime_to_format.hour)
        self.assertEqual(mi, self.datetime_to_format.minute)
        self.assertEqual(s, self.datetime_to_format.second)

    def test_date_failure(self):
        self.assertRaises(ValueError, lambda: format_datetime(self.date_to_fail))
