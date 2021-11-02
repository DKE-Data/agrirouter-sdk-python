from datetime import datetime


def now_as_utc_timestamp():
    return datetime.utcnow()


def now_as_utc_str():
    timestamp = datetime.utcnow()
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
