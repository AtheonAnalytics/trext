from unittest import TestCase

import mock
from os import path

from mock.mock import call

from trext.db.conn import AnyDB
from trext.extract.build import ExtractBuilder


class TestExtractBuilder(TestCase):
    def setUp(self):
        self.eb = ExtractBuilder()

    @mock.patch('trext.extract.build.tempfile.mkdtemp')
    @mock.patch('trext.extract.build.get_db_components')
    def test_build_tde_path(self, mock_db_comp, mock_mkdtmp):
        # data to test
        tmp_dir_path = "some_temp_dir"
        # mock necessary calls
        mock_mkdtmp.return_value = tmp_dir_path
        mock_db_comp.return_value = ('db', 'schema', 'view')
        # test building tde path
        self.eb._build_temp_tdepath()
        self.assertEqual(self.eb._tde_path, path.join(tmp_dir_path, 'view.tde'))

    @mock.patch('trext.extract.build.Extract')
    def test_initialise_extract(self, mock_extract):
        self.eb._initialise_extract()
        self.assertTrue(self.eb._extract, mock_extract)

    @mock.patch('trext.extract.build.DBConsumer')
    @mock.patch('trext.extract.build.TableDefinition')
    def test_build_skeleton(self, mock_table_def, mock_db_consumer):
        # data to test
        col_data = [
            ['col1', 1, 'sometype'],
            ['col2', 2, 'sometype'],
            ['col3', 3, 'sometype']
        ]
        expected_columns = {1: 'sometype', 2: 'sometype', 3: 'sometype'}
        # mock necessary calls
        mock_table_def.addColumn.return_type = ''
        mock_db_consumer.get_table_definition.return_value = col_data
        # test build skeleton
        self.eb._db_consumer = mock_db_consumer
        table_def = self.eb._build_skeleton()
        self.assertEqual(table_def, mock_table_def())
        self.assertEqual(self.eb.columns, expected_columns)
        self.assertEqual(mock_db_consumer.get_table_definition.call_count, 1)

    @mock.patch('trext.extract.build.TableDefinition')
    @mock.patch('trext.extract.build.Extract')
    @mock.patch('trext.extract.build.ExtractFiller')
    @mock.patch('trext.extract.build.DBConsumer')
    def test_fill_extract(self, mock_db_consumer, mock_extract_filler,
                          mock_extract, mock_table_def):
        # data to test
        dummy_data = [
            ['row1', 1, 2, 3],
            ['row2', 1, 2, 3],
            ['row3', 1, 2, 3],
        ]
        # mock relevant methods
        mock_db_consumer.get_table_data.return_value = dummy_data
        # test fill extract
        self.eb._db_consumer = mock_db_consumer
        self.eb._extract = mock_extract
        self.eb._fill_extract()
        self.assertEqual(mock_extract_filler.call_args_list[0],
                         call(
                             mock_extract.addTable(),
                             mock_table_def(),
                             {}
                         ))
        self.assertEqual(mock_extract_filler().insert_data_to_extract.call_count, 3)

    @mock.patch('trext.extract.build.AnyDB.get_cursor')
    def test_connection_to_db(self, mock_get_db_cursor):
        # data to test
        view_name = 'somedb.someschema.someview'
        conn_string = "some_connection_string"
        # set mock return values
        mock_get_db_cursor().return_value = ""
        # test connect_to_db
        self.eb.connect_to_db(view_or_table_name=view_name, conn_string=conn_string)
        self.assertEqual(self.eb._view_or_table_name, view_name)
        self.assertEqual(self.eb._db_type, None)
        self.assertEqual(self.eb._cursor, mock_get_db_cursor())
        self.assertTrue(isinstance(self.eb._db_conn, AnyDB))

    @mock.patch('trext.extract.build.ExtractFiller')
    @mock.patch('trext.extract.build.Extract')
    @mock.patch('trext.extract.build.TableDefinition')
    @mock.patch('trext.extract.build.DBConsumer')
    def test_create_extract(self, mock_db_consumer, mock_table_def,
                            mock_extract, mock_ef):
        # data to test
        cursor = "some cursor"
        view_name = 'somedb.someschema.someview'
        db_type = None
        # mock necessary methods
        self.eb._cursor = cursor
        self.eb._db_type = db_type
        self.eb._db_consumer = mock_db_consumer
        self.eb._view_or_table_name = view_name
        tde_path = self.eb.create_extract()
        # test create extract
        mock_db_consumer.assert_called_once_with(cursor, view_name, db_type)
        self.assertNotEqual(tde_path, None)

    @mock.patch('trext.extract.build.AnyDB')
    def test_close_when_connected(self, mock_db):
        self.eb._db_conn = mock_db
        self.eb.close()

    def test_close_when_not_connected(self):
        self.assertRaises(AttributeError, lambda: self.eb.close())
