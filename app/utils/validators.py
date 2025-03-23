from fastapi import HTTPException, status


def validate_positive_int64(value: int) -> int:
    try:
        value = int(value)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Value must be an integer.'
        )
    if value < 0 or value > 9223372036854775807:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Value must be a positive int64.'
        )
    return value


def validate_positive_int32(value: int) -> int:
    try:
        value = int(value)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Value must be an integer.'
        )
    if value < 0 or value > 2147483647:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Value must be a positive int32.'
        )
    return value


def validate_positive_smallint(value: int) -> int:
    try:
        value = int(value)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Value must be an integer.'
        )
    if value < 0 or value > 32767:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Value must be a positive smallint.'
        )
    return value


def validate_not_none(value):
    if value is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Value must not be None.'
        )

    return value


def validate_utf8_string(value: str) -> str:
    if '\x00' in value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Value contains null bytes, which are not allowed.'
        )
    try:
        value.encode('utf-8')
    except UnicodeEncodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Value contains invalid UTF-8 characters.'
        )

    return value
