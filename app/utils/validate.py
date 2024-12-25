def validate_positive_int64(value: int) -> int:
    if value < 0 or value > 9223372036854775807:
        raise ValueError('Value must be a positive int64.')

    return value


def validate_positive_int32(value: int) -> int:
    if value < 0 or value > 2147483647:
        raise ValueError('Value must be a positive int32.')

    return value


def validate_positive_smallint(value: int) -> int:
    if value < 0 or value > 32767:
        raise ValueError('Value must be a positive smallint.')

    return value
