from unittest import TestCase

import mock
from datetime import date, datetime

from mock.mock import Mock
from tableausdk.Extract import TableDefinition, Extract, Row
from tableausdk.Types import Type

from trext.db.fill import ExtractFiller
from trext.db.utils import get_fake_date, get_fake_datetime


class TestExtractFiller(TestCase):
    def setUp(self):
        self.table_def = TableDefinition()
        self.table_def.addColumn("int_1", Type.INTEGER)
        self.table_def.addColumn("int_2", Type.INTEGER)
        self.table_def.addColumn("date", Type.DATETIME)
        self.col_metadata = {
            1: Type.INTEGER,
            2: Type.INTEGER,
            3: Type.DATETIME,
        }

    def test_replace_null_functionality(self):
        rn = ExtractFiller._replace_null
        # boolean
        self.assertEqual(rn(Type.BOOLEAN, None), False)
        self.assertEqual(rn(Type.BOOLEAN, True), True)
        # integer
        self.assertEqual(rn(Type.INTEGER, None), 0)
        self.assertEqual(rn(Type.INTEGER, 12), 12)
        # float
        self.assertEqual(rn(Type.DOUBLE, None), 0.0)
        self.assertEqual(rn(Type.DOUBLE, 12.12), 12.12)
        # string
        self.assertEqual(rn(Type.CHAR_STRING, None), '')
        self.assertEqual(rn(Type.CHAR_STRING, 'somestring'), 'somestring')
        # unicode string
        self.assertEqual(rn(Type.UNICODE_STRING, None), u'')
        self.assertEqual(rn(Type.UNICODE_STRING, u'somestring'), u'somestring')
        # date
        self.assertEqual(rn(Type.DATE, None), get_fake_date())
        self.assertEqual(rn(Type.DATE, date(1990, 1, 1)), date(1990, 1, 1))
        # datetime
        self.assertEqual(rn(Type.DATETIME, None), get_fake_datetime())
        self.assertEqual(rn(Type.DATETIME, datetime(1990, 1, 1, 0, 0, 0, 0)),
                         datetime(1990, 1, 1, 0, 0, 0, 0))

    def test_replace_null_with_test_data(self):
        # row of data without NULLs
        test_data = [1, 2, datetime.today()]
        rn = ExtractFiller._replace_null
        for pos, db_datatype in self.col_metadata.iteritems():
            data = test_data[pos - 1]
            self.assertEqual(rn(db_datatype, data), data)
        # row of data with NULL
        test_data = [None, None, None]
        ret_val = [0, 0, get_fake_datetime()]
        for pos, db_datatype in self.col_metadata.iteritems():
            data = test_data[pos - 1]
            ret = ret_val[pos - 1]
            # should replace all NULLs
            self.assertNotEqual(rn(db_datatype, data), None)
            self.assertEqual(rn(db_datatype, data), ret)

    @mock.patch('trext.db.fill.Row')
    @mock.patch('tableausdk.Extract.Extract')
    def test_insert_data(self, mock_extract, mock_row):
        test_data = [1, 2, datetime.today()]
        # get a mock extract and add table
        mock_extract = mock_extract.return_value
        mock_extract.addTable('test_extract', self.table_def)
        # create instance of class to test
        self.ef = ExtractFiller(mock_extract, self.table_def, self.col_metadata)
        self.ef.insert_data_to_extract(test_data)
        # test call argument
        mock_row.assert_called_with(self.table_def)
        row_to_insert = mock_row.return_value
        # test insert methods called for test data
        self.assertEqual(row_to_insert.setInteger.call_count, 2)
        self.assertEqual(row_to_insert.setDateTime.call_count, 1)
