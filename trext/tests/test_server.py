from unittest import TestCase
import mock

from trext.extract.server import Tableau


class TestTableauServer(TestCase):
    @mock.patch('trext.extract.server.ServerConnection')
    @mock.patch('trext.extract.server.ServerAPI')
    def test_connect(self, mock_serv, mock_serv_conn):
        # data to test with
        host = "test"
        username = "tableau_server_username"
        password = "something_secure"
        # test connect
        tableau_server = Tableau()
        tableau_server.connect(host, username, password)
        mock_serv_conn().connect.assert_called_once_with(host, username, password, 'Default')

    @mock.patch('trext.extract.server.ServerConnection')
    @mock.patch('trext.extract.server.ServerAPI')
    def test_publish(self, mock_serv, mock_serv_conn):
        # data to test with
        tde_path = "some/path/to/file.tde"
        tableau_server = Tableau()
        tableau_server.publish(tde_path)
        mock_serv_conn().publishExtract.assert_called_once_with(tde_path, 'Default', 'file', True)

    @mock.patch('trext.extract.server.ServerConnection')
    @mock.patch('trext.extract.server.ServerAPI')
    def test_close(self, mock_serv, mock_serv_conn):
        tableau_server = Tableau()
        tableau_server.close()
        mock_serv_conn().disconnect.assert_called_once()
        mock_serv().cleanup.assert_called_once()
