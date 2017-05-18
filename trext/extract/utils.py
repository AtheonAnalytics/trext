import re


def get_db_components(dbtable):
    db_component_regex = re.compile('([\[^[][\w\.]+\]?|[\w]+)')
    # Split the table path into its components
    components = re.findall(db_component_regex, dbtable)
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
