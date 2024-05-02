import uuid


class UUIDUtil:

    @staticmethod
    def new_uuid():
        """

        UUIDUtil.new_uuid() -> str

        Generates a new universally unique identifier (UUID) and returns it as a string representation.

        Returns:
            str: A string representation of the generated UUID.

        Example:
            >>> UUIDUtil.new_uuid()
            'c5616b83-733b-4500-8c7a-efbff81b226b'
        """
        return str(uuid.uuid4())
