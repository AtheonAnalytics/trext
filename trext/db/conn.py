import pyodbc


def _get_connector(dbtype=None):
    connector = None
    if not dbtype:
        connector = pyodbc
    if dbtype == 'exasol':
        # todo need to document and extend this
        connector = __import__('exasol')
    return connector


class AnyDB(object):
    def __init__(self, connection_string, dbtype=None):
        self._db_connection_string = connection_string
        self._db_type = dbtype
        self._db_connection = None
        self._db_cursor = None

    def get_cursor(self):
        connection_library = _get_connector(self._db_type)
        self._db_connection = connection_library.connect(self._db_connection_string)
        self._db_cursor = self._db_connection.cursor()
        return self._db_cursor

    def close(self):
        self._db_connection.close()
