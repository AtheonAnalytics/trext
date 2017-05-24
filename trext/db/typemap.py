from tableausdk.Types import Type

_type = dict()

# MSSQL types
_type['int'] = Type.INTEGER
_type['bigint'] = Type.INTEGER
_type['tinyint'] = Type.INTEGER
_type['smallint'] = Type.INTEGER
_type['bit'] = Type.BOOLEAN
_type['binary'] = Type.CHAR_STRING
_type['char'] = Type.CHAR_STRING
_type['varchar'] = Type.UNICODE_STRING
_type['nvarchar'] = Type.UNICODE_STRING
_type['date'] = Type.DATE
_type['datetime'] = Type.DATETIME
_type['decimal'] = Type.DOUBLE
_type['numeric'] = Type.DOUBLE

# EXAsol types
_type['double'] = Type.DOUBLE
_type['boolean'] = Type.BOOLEAN
_type['timestamp'] = Type.DATETIME


def get_type(db_type):
    """
    Method to map the database column type to the Tableau SDK Type
    
    :param db_type: types that may have length in the declaration 
    eg: CHAR(8)  
    :return: Tableau SDK Type if it exists  
    """
    mapped_type = [tm for key, tm in _type.iteritems() if db_type.lower().startswith(key)]
    if len(mapped_type) == 1:  # one match
        return mapped_type[0]
    elif len(mapped_type) == 0:  # no match
        return None
    else:  # multiple matches
        return next(iter(tm for key, tm in _type.iteritems() if db_type.lower() == key), None)


if __name__ == '__main__':
    print get_type('DECIMAL(18,2)')
    print get_type('datetime')
