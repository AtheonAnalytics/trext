from trext.db.typemap import get_type
from trext.extract.utils import get_db_components


class DBConsumer(object):
    """
    Pulls the db/view metadata and data from the database. 
    """

    def __init__(self, cursor, view_or_table_name, dbtype):
        self._cursor = cursor
        self._dbtype = dbtype
        self._db, self._schema, self._table = get_db_components(view_or_table_name)

    def _get_db_column_metadata(self):
        res = None
        # default None is mssql
        if not self._dbtype:
            res = self._cursor.execute('''
            SELECT      COLUMN_NAME, DATA_TYPE, ORDINAL_POSITION
            FROM        %s.INFORMATION_SCHEMA.COLUMNS
            WHERE        (TABLE_SCHEMA = '?') and (TABLE_NAME = '?')
            ORDER BY ORDINAL_POSITION
            ''' % self._db, (self._schema, self._table))
        elif self._dbtype == 'exasol':
            self._cursor.execute("OPEN SCHEMA %s;" % self._schema)
            res = self._cursor.execute("DESCRIBE %s.%s;" % (self._schema, self._table))
        return res

    def _get_db_data(self):
        res = None
        if not self._dbtype:
            res = self._cursor.execute('''SELECT * FROM %s.%s.%s
            ''' % (self._db, self._schema, self._table))
        elif self._dbtype == 'exasol':
            self._cursor.execute("OPEN SCHEMA %s;" % self._schema)
            res = self._cursor.execute('SELECT * FROM %s.%s;' % (self._schema, self._table))
        return res

    def get_table_definition(self):
        res = self._get_db_column_metadata()
        try:
            position = 1
            for data in res.fetchall():
                field_name = data[0]
                field_type = data[1]
                try:
                    field_type = get_type(field_type)
                except:
                    print "failed field type", data
                    field_type = 15
                yield field_name, position, field_type
                position += 1
        except Exception as e:
            # todo better error handling
            raise e

    def get_table_data(self):
        try:
            res = self._get_db_data()
            while True:
                data = res.fetchmany(1000)
                if not data:
                    break
                for row in data:
                    yield row
        except Exception as e:
            # todo better error handling
            raise e
