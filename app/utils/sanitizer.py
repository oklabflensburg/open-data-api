def sanitize_string(value: str) -> str:
    if '\x00' in value:
        raise ValueError('Invalid character detected.')

    return value.strip()


def sanitize_dict(data: dict) -> dict:
    return {k: sanitize_string(v) if isinstance(v, str) else v for k, v in data.items()}