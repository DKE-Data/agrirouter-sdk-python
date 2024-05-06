from datetime import datetime, timedelta

from google.protobuf.timestamp_pb2 import Timestamp

from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import ValidityPeriod


class UtcTimeUtil:

    @staticmethod
    def now_as_utc_timestamp() -> datetime:
        """
        Returns current utc timestamp
        """
        return datetime.utcnow()

    @staticmethod
    def now_as_utc_str() -> str:
        """
        Returns current utc timestamp as a string
        """
        timestamp = datetime.utcnow()
        return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @staticmethod
    def max_validity_period() -> ValidityPeriod:
        """
        Returns time stamp from weeks before according to the Timestamp protobuf format
        """
        return ValidityPeriod(sent_from=UtcTimeUtil._timestamp_before_number_of_weeks(4),
                              sent_to=UtcTimeUtil._now_as_timestamp())

    @staticmethod
    def validity_period_for_seconds(seconds) -> ValidityPeriod:
        """
        Returns validity period from seconds before according to the ValidityPeriod protobuf format
        """
        return ValidityPeriod(sent_from=UtcTimeUtil._timestamp_before_number_of_seconds(seconds),
                              sent_to=UtcTimeUtil._now_as_timestamp())

    @staticmethod
    def validity_period_for_weeks(weeks) -> ValidityPeriod:
        """
        Returns validity period from seconds before according to the ValidityPeriod protobuf format
        """
        return ValidityPeriod(sent_from=UtcTimeUtil._timestamp_before_number_of_weeks(weeks),
                              sent_to=UtcTimeUtil._now_as_timestamp())

    @staticmethod
    def _timestamp_before_number_of_weeks(weeks) -> Timestamp:
        """
        Returns time stamp from weeks before according to the Timestamp protobuf format
        """
        utc_timestamp_weeks_ago = datetime.now() - timedelta(weeks=weeks)
        sent_from = Timestamp()
        sent_from.seconds = int(utc_timestamp_weeks_ago.timestamp())
        sent_from.nanos = utc_timestamp_weeks_ago.microsecond * 1000
        return sent_from

    @staticmethod
    def _timestamp_before_number_of_seconds(seconds) -> Timestamp:
        """
        Returns time stamp from seconds before according to the Timestamp protobuf format.
        This is used to test the invalid validity period and is only used for testing purposes
        """
        utc_timestamp_seconds_ago = datetime.now() - timedelta(seconds=seconds)
        sent_from = Timestamp()
        sent_from.seconds = int(utc_timestamp_seconds_ago.timestamp())
        sent_from.nanos = utc_timestamp_seconds_ago.microsecond * 1000
        return sent_from

    @staticmethod
    def _now_as_timestamp():
        """
        Returns current time stamp in google protobuf format
        """
        sent_to = Timestamp()
        sent_to.seconds = int(datetime.now().timestamp())
        sent_to.nanos = datetime.now().microsecond * 1000
        return sent_to
