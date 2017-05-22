import os
import tempfile

from tableausdk.Extract import Extract, TableDefinition

from trext.db.conn import AnyDB
from trext.db.consume import DBConsumer
from trext.db.fill import ExtractFiller
from trext.extract.utils import get_db_components


class ExtractBuilder(object):
    """
    Builds the tableau Extract by creating a Tableau Extract, defines the table skeleton, adds the 
    table to the extract and fills this table with the relevant data for the TDE. 
    """

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
        """
        creates a temporary directory and defines the tde path as temp_dir+view_or_table_name.tde
        """
        temp_dir_path = tempfile.mkdtemp()
        _, __, extract_name = get_db_components(self._view_or_table_name)
        file_name = "{}.tde".format(extract_name)
        self._tde_path = os.path.join(temp_dir_path, file_name)

    def _initialise_extract(self):
        """
        initialises extract with the defined tde path
        """
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
        """
        Assigns the table definition (skeleton) to the extract
         
        :param table_def: the skeleton of the view or table
        :return: updated tableau `Extract`
        """
        return self._extract.addTable('Extract', table_def)

    def _fill_extract(self):
        """
        Fills the Extract with data from the view/table
        """
        extract_table_definition = self._build_skeleton()
        tde_table = self._add_table_to_extract(extract_table_definition)
        extract_feed = ExtractFiller(tde_table, extract_table_definition, self.columns)
        for row in self._db_consumer.get_table_data():
            extract_feed.insert_data_to_extract(row)
        self._extract.close()

    def connect_to_db(self, view_or_table_name, conn_string, dbtype=None):
        """
        Connect to the view or table that needs to be turned into a .tde extract
        
        :param view_or_table_name: View or Table that needs to be an extract
        :param conn_string: connection string to the database where the view or table exists
        :param dbtype: type of db so the right pyodbc wrapper is used to connect
        """
        self._db_conn = AnyDB(conn_string, dbtype)
        self._cursor = self._db_conn.get_cursor()
        self._db_type = dbtype
        self._view_or_table_name = view_or_table_name

    def create_extract(self):
        """
        Creates the extract by 
        - connecting to the database,
        - building the tde path
        - initializing the extract
        - pulling data from db and filling the extract
        
        :return: path to the created .tde extract 
        """
        self._db_consumer = DBConsumer(self._cursor, self._view_or_table_name, self._db_type)
        self._build_temp_tdepath()
        self._initialise_extract()
        self._fill_extract()
        return self._tde_path

    def close(self):
        self._db_conn.close()
