from unittest import TestCase
from datetime import date, datetime

from trext.db.utils import format_date, format_datetime, get_fake_date, get_fake_datetime
from trext.extract.exceptions import NotExtractPathError
from trext.extract.utils import get_extract_name, get_db_components


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


def test_fake_date():
    assert get_fake_date().year == 1900
    assert get_fake_date().month == 01
    assert get_fake_date().day == 01


def test_fake_datetime():
    assert get_fake_datetime().year == 1900
    assert get_fake_datetime().month == 01
    assert get_fake_datetime().day == 01
    assert get_fake_datetime().hour == 0
    assert get_fake_datetime().minute == 0
    assert get_fake_datetime().second == 0
    assert get_fake_datetime().microsecond == 0


class TestDBComponents(TestCase):
    def test_get_db_component_parts(self):
        components = get_db_components("some_db.some_schema.some_table")
        self.assertEqual(components, ("some_db", "some_schema", "some_table"))
        components = get_db_components("some_schema.some_table")
        self.assertEqual(components, (None, "some_schema", "some_table"))

    def test_get_db_component_exception(self):
        self.assertRaises(NotImplementedError,
                          lambda: get_db_components("some_table"))

        self.assertRaises(NotImplementedError,
                          lambda: get_db_components(
                              "some_db.some_node.some_schema.some_table"))


class TestExtractName(TestCase):
    def test_get_extract_name_from_tde(self):
        tde_path = "path/to/some/extract.tde"
        extract = get_extract_name(tde_path)
        assert extract == 'extract'

    def test_get_extract_name_from_non_tde(self):
        not_tde_path = "path/to/some/extract.someotherextension"
        self.assertRaises(NotExtractPathError,
                          lambda: get_extract_name(not_tde_path))
