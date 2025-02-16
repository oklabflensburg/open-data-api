import re

from datetime import datetime



def parse_date(date_str: str):
    date_str = date_str.strip()

    # Match optional operators (<, >, =) before the date
    match = re.match(r'([<>]=?|=)?\s*(\d{4}|\d{2}\.\d{4}|\d{2}\.\d{2}\.\d{4})$', date_str)
    
    if not match:
        raise ValueError(f'Unknown date format: {date_str}')

    operator, date_value = match.groups()
    operator = operator or '='  # Default to '=' if no operator is provided

    # Parse date formats
    try:
        if re.match(r'^\d{4}$', date_value):  # Year only
            return datetime.strptime(date_value, '%Y'), operator
        elif re.match(r'^\d{2}\.\d{4}$', date_value):  # Month.Year
            return datetime.strptime(date_value, '%m.%Y'), operator
        elif re.match(r'^\d{2}\.\d{2}\.\d{4}$', date_value):  # Day.Month.Year
            return datetime.strptime(date_value, '%d.%m.%Y'), operator
    except ValueError:
        raise ValueError(f'Invalid date format: {date_str}')

    raise ValueError(f'Unknown date format: {date_str}')
