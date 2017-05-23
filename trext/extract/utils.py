import re

from trext.extract.exceptions import NotExtractPathError


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


def get_extract_name(extract_path):
    """
    Get the name of the extract in the format - name.tde

    :param extract_path: Path where the extract sits
    :return: 
    """
    extract_name_regex = re.compile("(\w*).tde$")
    try:
        extract_name = extract_name_regex.findall(extract_path)[0]
    except IndexError:
        raise NotExtractPathError
    return extract_name
