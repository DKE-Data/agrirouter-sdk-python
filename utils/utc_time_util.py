from datetime import datetime


def now_as_utc_timestamp():
    timestamp = datetime.utcnow()
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
