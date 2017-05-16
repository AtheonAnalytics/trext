from tableausdk.Types import Type

_type = dict()

# MSSQL types
_type['nvarchar'] = Type.UNICODE_STRING
_type['int'] = Type.INTEGER
_type['bigint'] = Type.INTEGER
_type['tinyint'] = Type.INTEGER
_type['smallint'] = Type.INTEGER
_type['bit'] = Type.BOOLEAN
_type['binary'] = Type.CHAR_STRING
_type['char'] = Type.CHAR_STRING
_type['varchar'] = Type.CHAR_STRING
_type['date'] = Type.DATE
_type['datetime'] = Type.DATETIME
_type['decimal'] = Type.DOUBLE
_type['numeric'] = Type.DOUBLE

# EXAsol types
_type['DECIMAL'] = Type.DOUBLE
_type['DOUBLE'] = Type.DOUBLE
_type['VARCHAR'] = Type.UNICODE_STRING
_type['CHAR'] = Type.CHAR_STRING
_type['DATE'] = Type.DATE
_type['BOOLEAN'] = Type.BOOLEAN
_type['DATE'] = Type.DATE


def get_type(db_type):
    """
    Method to map the database column type to the Tableau SDK Type
    
    :param db_type: types that may have length in the declaration 
    eg: CHAR(8)  
    :return: Tableau SDK Type if it exists  
    """
    # todo needs error handling
    return next(iter(type_map for key, type_map in _type.iteritems() if key in db_type), None)


if __name__ == '__main__':
    print get_type('DECIMAL(18,2)')
    print get_type('date')
