import re


def get_db_components(db_table_or_view):
    """
    Splits the db_table into 3 components - db, schema and table/view
    
    :param db_table_or_view: of the form [DB].[SCHEMA].[TABLE]
    :return: tuple of db, schema and table
    """
    db_component_regex = re.compile('([\[^[][\w\.]+\]?|[\w]+)')
    # Split the table path into its components
    components = re.findall(db_component_regex, db_table_or_view)
    if len(components) == 2:
        db = None
        schema, table = components
    elif len(components) == 3:
        db, schema, table = components
    else:
        raise NotImplementedError
    # get the table and the schema names
    schema = schema.replace('[', '').replace(']', '')
    table = table.replace('[', '').replace(']', '')
    return db, schema, table
