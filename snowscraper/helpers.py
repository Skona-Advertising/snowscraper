from datetime import datetime


def string_to_datetime(date_string):
    try:
        # try ISO 8601
        if "Z" in date_string:
            return datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return datetime.fromisoformat(date_string)
    except ValueError:
        pass

    try:
        # try RFC 1123
        return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z")
    except ValueError:
        pass

    raise ValueError(f"Unsupported date format: {date_string}")
