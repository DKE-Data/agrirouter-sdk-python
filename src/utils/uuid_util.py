import uuid


def new_uuid():
    """

    new_uuid() -> str

    Generates a new universally unique identifier (UUID) and returns it as a string representation.

    Returns:
        str: A string representation of the generated UUID.

    Example:
        >>> new_uuid()
        'c5616b83-733b-4500-8c7a-efbff81b226b'
    """
    return str(uuid.uuid4())
