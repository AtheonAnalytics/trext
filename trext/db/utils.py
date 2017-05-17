import time


def format_datetime(datetime_to_format):
    """
    Formats the datetime value from database to the tableau format
    
    :param datetime_to_format: datetime value from db 
    :return: formatted datetime
    """
    datetime_to_format = str(datetime_to_format)
    try:
        date_conv = time.strptime(datetime_to_format, '%Y-%m-%d %H:%M:%S.%f')[:7]
    except ValueError:
        date_conv = time.strptime(datetime_to_format, '%Y-%m-%d %H:%M:%S')[:7]
    return date_conv


def format_date(date_to_format):
    """
    Formats the date value from database to the tableau format
    
    :param date_to_format: date value from db
    :return: formatted date
    """
    date_to_format = str(date_to_format)
    return time.strptime(date_to_format, '%Y-%m-%d')[:3]