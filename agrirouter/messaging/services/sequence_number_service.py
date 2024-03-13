from typing import Dict


class SequenceNumberService:
    """
    Service to generate sequence numbers while sending messages to the agrirouter. The sequence
    number generation is based on the ID of the endpoint, therefore a sequence number can be used
    multiple times for different endpoints.
    """
    sequence_numbers_for_endpoints: Dict[str, int] = {}

    @staticmethod
    def next_seq_nr(endpoint_id: str) -> int:
        """
        Generate sequence number for the endpoint_id
        params: endpoint_id
        returns: 1 if 1st call, 1+n if nth call
        """
        SequenceNumberService.sequence_numbers_for_endpoints[
            endpoint_id] = SequenceNumberService.sequence_numbers_for_endpoints.setdefault(endpoint_id, 0) + 1
        return SequenceNumberService.sequence_numbers_for_endpoints[endpoint_id]
