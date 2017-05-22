from tableausdk.Exceptions import TableauException
from tableausdk.Extract import Row
from tableausdk.Types import Type

from trext.db.utils import format_datetime, format_date, get_fake_date, get_fake_datetime


class ExtractFiller(object):
    """
    Fills the extract skeleton with cleaned and formatted data.
    
    """

    def __init__(self, table, table_definition, column_metadata):
        """
        :param table: Tableau table to insert data into
        :param table_definition: definition of the extract
        :param column_metadata: the metadata about the columns - the name, position and type of 
        the columns in the view or table type mapped to Tableau SDK types. See 
        `tableausdk.Types.Type` and `trext.db.typemap` for more information. 
        """
        self._table = table
        self._table_definition = table_definition
        self._column_metadata = column_metadata

    @staticmethod
    def _replace_null(col_type, col_data):
        """
        Replaces the null data with values based on type. Eg: 0 if integer and 0.0 if float.
        If there is no null data then it returns the existing value, col_data.
        
        Note:
        1. This will need more suitable values as db NULLs are more useful than a replaced value.
        
        :param col_type: type of the column to decide what value to replace
        :param col_data: the value in the column that needs checking
        :return: cleaned up column_data
        """
        null_replacement_map = {
            Type.INTEGER: 0,
            Type.BOOLEAN: False,
            Type.CHAR_STRING: '',
            Type.UNICODE_STRING: u'',
            Type.DATE: get_fake_date(),
            Type.DATETIME: get_fake_datetime(),
            Type.DOUBLE: 0.0
        }
        return null_replacement_map.get(col_type) if col_data is None else col_data

    def insert_data_to_extract(self, db_data_row):
        """
        Inserts the data row by row into the tableau extract skeleton
        
        :param db_data_row: row from the database
        """
        # Get the row of data to insert
        insert_row = Row(self._table_definition)
        # Map the column type to the TDE insert function
        extract_type_map = {
            Type.INTEGER: insert_row.setInteger,
            Type.DOUBLE: insert_row.setDouble,
            Type.BOOLEAN: insert_row.setBoolean,
            Type.DATE: insert_row.setDate,
            Type.DATETIME: insert_row.setDateTime,
            Type.CHAR_STRING: insert_row.setCharString,
            Type.UNICODE_STRING: insert_row.setString,
        }
        # Iterate through each column of the row to identify the type
        for column_pos, column_type in self._column_metadata.iteritems():
            extract_col_pos_ = column_pos - 1
            insert_row.Insert = extract_type_map[column_type]

            # If there is any NULL data replace with corresponding NULL type data for the field
            column_data = db_data_row[extract_col_pos_]
            column_data = self._replace_null(column_type, column_data)

            # Identify the insert function for the data
            try:
                # Date time field
                if column_type == 13:
                    year, month, day, hour, minute, sec, frac = format_datetime(column_data)
                    insert_row.Insert(extract_col_pos_, year, month, day, hour, minute, sec, frac)
                # Date field
                elif column_type == 12:
                    year, month, day = format_date(column_data)
                    insert_row.Insert(extract_col_pos_, year, month, day)
                # Other fields
                else:
                    insert_row.Insert(extract_col_pos_, column_data)
            except TableauException as e:
                raise e
        # Insert the row
        self._table.insert(insert_row)
        insert_row.close()
