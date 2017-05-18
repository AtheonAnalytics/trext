import os
import tempfile

from tableausdk.Extract import Extract, TableDefinition

from trext.db.conn import AnyDB
from trext.db.consume import DBConsumer
from trext.db.fill import ExtractFiller


class ExtractBuilder(object):
    def __init__(self):
        self._db_type = None
        self._db_conn = None
        self._cursor = None
        self._view_or_table_name = None
        self._extract = None
        self.columns = dict()
        self._db_consumer = None
        self._tde_path = None

    def _build_temp_tdepath(self):
        temp_dir_path = tempfile.mkdtemp()
        file_name = "{}.tde".format(self._view_or_table_name)
        self._tde_path = os.path.join(temp_dir_path, file_name)

    def _initialize_extract(self):
        self._extract = Extract(self._tde_path)

    def _build_skeleton(self):
        """
        Gets the columns from the table or view and then auto builds the Tableau
        table definition - the skeleton of the extract we want to create
        
        :return: table_def: Tableau table definition
        """
        table_def = TableDefinition()
        db_table_columns = self._db_consumer.get_table_definition()
        for field_name, position, field_type in db_table_columns:
            table_def.addColumn(field_name, field_type)
            self.columns[position] = field_type
        return table_def

    def _add_table_to_extract(self, table_def):
        return self._extract.addTable('Extract', table_def)

    def _feed_skeleton(self):
        extract_table_definition = self._build_skeleton()
        tdetable = self._add_table_to_extract(extract_table_definition)
        extract_feed = ExtractFiller(tdetable, extract_table_definition, self.columns)
        for row in self._db_consumer.get_table_data():
            extract_feed.insert_data_to_extract(row)
        self._extract.close()

    def connect_to_db(self, view_or_table_name, conn_string, dbtype=None):
        self._db_conn = AnyDB(conn_string, dbtype)
        self._cursor = self._db_conn.get_cursor()
        self._db_type = dbtype
        self._view_or_table_name = view_or_table_name

    def create_extract(self):
        self._db_consumer = DBConsumer(self._cursor, self._view_or_table_name, self._db_type)
        self._build_temp_tdepath()
        self._initialize_extract()
        self._feed_skeleton()
        return self._tde_path

    def close(self):
        self._db_conn.close()
