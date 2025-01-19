from ..utils.exceptions import CustomValidationError



def validate_positive_int64(value: int, field_location: str, field_name: str) -> int:
    if value < 0 or value > 9223372036854775807:
        raise CustomValidationError(
            loc=[field_location, field_name],
            msg='Value must be a positive int64.',
            error_type='value_error.integer'
        )

    return value


def validate_positive_int32(value: int, field_location: str, field_name: str) -> int:
    if value < 0 or value > 2147483647:
        raise CustomValidationError(
            loc=[field_location, field_name],
            msg='Value must be a positive int32.',
            error_type='value_error.integer'
        )

    return value


def validate_positive_smallint(value: int, field_location: str, field_name: str) -> int:
    if value < 0 or value > 32767:
        raise CustomValidationError(
            loc=[field_location, field_name],
            msg='Value must be a positive smallint.',
            error_type='value_error.integer'
        )

    return value


def validate_not_none(value, field_location: str, field_name: str):
    if value is None:
        raise CustomValidationError(
            loc=[field_location, field_name],
            msg=f'{field_name} must not be None.',
            error_type='value_error.integer'
        )

    return value
