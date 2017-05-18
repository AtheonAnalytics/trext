from datetime import datetime, date

from tableausdk.Exceptions import TableauException
from tableausdk.Extract import Row

from trext.db.utils import format_datetime, format_date


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
    def _replace_null(column_type, column_data):
        """
        Replaces the null data with values based on type. Eg: 0 if integer and 0.0 if float.
        
        Note:
        1. This will need more suitable values as db NULLs are more useful than a replaced value.
        2. A switch-case type statement might (will most certainly?) be more efficient
        
        :param column_type: type of the column to decide what value to replace
        :param column_data: the value in the column that needs checking
        :return: cleaned up column_data
        """
        # integer
        column_data = 0 if (
            column_data is None and (column_type == 7 or column_type == 11)) else column_data
        # decimal or float
        column_data = 0.0 if (column_data is None and column_type == 10) else column_data
        # string
        column_data = '' if (
            column_data is None and (column_type == 15 or column_type == 16)) else column_data
        # datetime
        column_data = datetime.now() if (
            column_data is None and column_type == 13) else column_data
        # date
        column_data = date.today() if (
            column_data is None and column_type == 12) else column_data
        return column_data

    def insert_data_to_extract(self, db_data_row):
        """
        Inserts the data row by row into the tableau extract skeleton
        
        :param db_data_row: row from the database
        """
        # Get the row of data to insert
        insert_row = Row(self._table_definition)
        # Map the column type to the TDE insert function
        extract_type_map = {
            7: insert_row.setInteger,
            10: insert_row.setDouble,
            11: insert_row.setBoolean,
            12: insert_row.setDate,
            13: insert_row.setDateTime,
            15: insert_row.setCharString,
            16: insert_row.setString,
        }
        # Iterate through each column of the row to identify the type
        # # Note:     This probably can be split into two parts: one to identify the
        # # structure of the object to be inserted
        # #  and other to insert all the rows following the same rule.
        # # The procedure below is quite redundant.
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
