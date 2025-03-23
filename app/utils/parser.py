import re

from fastapi import HTTPException, status
from datetime import datetime


def parse_date(date_str: str):
    if not date_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Date string cannot be None or empty'
        )

    date_str = date_str.strip()

    match = re.match(
        r'([<>]=?|=)?\s*(\d{4}|\d{2}\.\d{4}|\d{2}\.\d{2}\.\d{4})$', date_str)

    if not match:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Unknown date format: {date_str}'
        )

    operator, date_value = match.groups()
    operator = operator or '='

    try:
        if re.match(r'^\d{4}$', date_value):
            return datetime.strptime(date_value, '%Y'), operator
        elif re.match(r'^\d{2}\.\d{4}$', date_value):
            return datetime.strptime(date_value, '%m.%Y'), operator
        elif re.match(r'^\d{2}\.\d{2}\.\d{4}$', date_value):
            return datetime.strptime(date_value, '%d.%m.%Y'), operator
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Invalid date format: {date_str}'
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Unknown date format: {date_str}'
    )
