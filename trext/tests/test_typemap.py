from unittest import TestCase

from tableausdk.Types import Type

from trext.db.typemap import get_type


class TestTypeMapper(TestCase):
    def test_unicode_string(self):
        self.assertEqual(get_type('nvarchar(255)'), Type.UNICODE_STRING)
        self.assertEqual(get_type('varchar(255)'), Type.UNICODE_STRING)
        self.assertEqual(get_type('VARCHAR(255)'), Type.UNICODE_STRING)

    def test_char_string(self):
        self.assertEqual(get_type('char(10)'), Type.CHAR_STRING)
        self.assertEqual(get_type('CHAR(100)'), Type.CHAR_STRING)
        self.assertEqual(get_type('binary'), Type.CHAR_STRING)

    def test_integer(self):
        self.assertEqual(get_type('int'), Type.INTEGER)
        self.assertEqual(get_type('bigint'), Type.INTEGER)
        self.assertEqual(get_type('tinyint'), Type.INTEGER)
        self.assertEqual(get_type('smallint'), Type.INTEGER)

    def test_double(self):
        self.assertEqual(get_type('decimal(18,2)'), Type.DOUBLE)
        self.assertEqual(get_type('DECIMAL(18,2)'), Type.DOUBLE)
        self.assertEqual(get_type('DOUBLE'), Type.DOUBLE)

    def test_date(self):
        self.assertEqual(get_type('date'), Type.DATE)
        self.assertEqual(get_type('datetime'), Type.DATETIME)
        self.assertEqual(get_type('DATETIME'), Type.DATETIME)
        self.assertEqual(get_type('TIMESTAMP'), Type.DATETIME)

    def test_boolean(self):
        self.assertEqual(get_type('bit'), Type.BOOLEAN)
        self.assertEqual(get_type('BOOLEAN'), Type.BOOLEAN)
