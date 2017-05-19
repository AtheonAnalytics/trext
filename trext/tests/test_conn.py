from unittest import TestCase

import mock

from trext.db.conn import AnyDB


class TestConnectionDefault(TestCase):
    def setUp(self):
        self.conn_string = "DSN=some_db_connection_string"
        self.adb = AnyDB(self.conn_string)

    @mock.patch('trext.db.conn.pyodbc')
    def test_is_connected_to_conn_string(self, mock_pyodbc):
        self.adb.get_cursor()
        mock_pyodbc.connect.assert_called_with(self.conn_string)

    @mock.patch('trext.db.conn.pyodbc')
    def test_close_connection(self, mock_pyodbc):
        self.adb.get_cursor()
        self.adb.close()
        mock_pyodbc.connect().close.assert_called()


class TestConnectionExasol(TestCase):
    def setUp(self):
        self.conn_string = "DSN=some_db_connection_string"
        self.adb = AnyDB(self.conn_string, dbtype='exasol')

    def test_is_connected_to_conn_string(self):
        connector = mock.MagicMock()
        with mock.patch.dict(
                'sys.modules',
                {'exasol': connector}
        ):
            self.adb.get_cursor()
            connector.connect.assert_called()
            connector.connect.assert_called_with(self.conn_string)

    def test_close_connection(self):
        connector = mock.MagicMock()
        with mock.patch.dict(
                'sys.modules',
                {'exasol': connector}
        ):
            self.adb.get_cursor()
            self.adb.close()
            connector.connect().close.assert_called()
