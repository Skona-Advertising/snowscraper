from datetime import datetime

def unix_to_datetime_utc(timestamp_millis):
    # Convert to seconds from milliseconds
    timestamp_seconds = timestamp_millis / 1000.0
    
    # Create a datetime object in UTC
    dt_object = datetime.utcfromtimestamp(timestamp_seconds)
    
    # Format the datetime object as an ISO 8601 string
    return dt_object.isoformat() + 'Z'  # 'Z' indicates UTC time


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
