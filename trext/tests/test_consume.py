import types
import mock
from unittest import TestCase

from trext.db.consume import DBConsumer


class TestDBConsumerDefault(TestCase):
    @mock.patch('trext.db.consume.get_db_components')
    def test_get_db_table_definition_return_type(self, mock_get_dbcomps):
        mock_get_dbcomps.return_value = ('db', 'schema', 'table')
        db_consumer = DBConsumer('', '', None)
        res = db_consumer.get_table_definition()
        self.assertTrue(isinstance(res, types.GeneratorType))

    @mock.patch('trext.db.consume.get_db_components')
    def test_get_db_table_data_return_type(self, mock_get_dbcomps):
        mock_get_dbcomps.return_value = ('db', 'schema', 'table')
        db_consumer = DBConsumer('', '', None)
        res = db_consumer.get_table_data()
        self.assertTrue(isinstance(res, types.GeneratorType))
