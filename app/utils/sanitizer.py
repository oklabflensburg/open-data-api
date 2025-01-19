import re


def sanitize_string(value: str) -> str:
    # Remove non-printable characters (any character with a hex value < 32 or > 127)
    if not value.isprintable():
        raise ValueError('Invalid non-printable character detected.')

    # Matches non-ASCII printable characters
    sanitized_value = re.sub(r'[^\x20-\x7E]', '', value)

    return sanitized_value.strip()


def sanitize_dict(data: dict) -> dict:
    return {k: sanitize_string(v) if isinstance(v, str) else v for k, v in data.items()}
