from datetime import datetime, timedelta
from google.protobuf.timestamp_pb2 import Timestamp


def now_as_utc_timestamp():
    """
    Returns current utc timestamp
    """
    return datetime.utcnow()


def now_as_utc_str():
    """
    Returns current utc timestamp as a string
    """
    timestamp = datetime.utcnow()
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def protobuf_timestamp_before_number_of_weeks(weeks):
    """
    Returns time stamp from weeks before according in the Timestamp protobuf format
    """
    utc_timestamp_weeks_ago = datetime.utcnow() - timedelta(weeks=weeks)
    sent_from = Timestamp()
    sent_from.seconds = int(utc_timestamp_weeks_ago.timestamp())
    sent_from.nanos = utc_timestamp_weeks_ago.microsecond * 1000
    return sent_from


def now_as_timestamp_protobuf():
    """
    Returns current time stamp in google protobuf format
    """
    sent_to = Timestamp()
    sent_to.seconds = int(datetime.utcnow().timestamp())
    sent_to.nanos = datetime.utcnow().microsecond * 1000
    return sent_to


def protobuf_timestamp_before_few_seconds(seconds):
    """
    Returns time stamp from seconds before according in the Timestamp protobuf format.
    This is used to test the invalid validity period and is only used for testing purposes
    """
    utc_timestamp_weeks_ago = datetime.utcnow() - timedelta(seconds=seconds)
    sent_from = Timestamp()
    sent_from.seconds = int(utc_timestamp_weeks_ago.timestamp())
    sent_from.nanos = utc_timestamp_weeks_ago.microsecond * 1000
    return sent_from
