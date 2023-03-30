from typing import Dict
from agrirouter.onboarding.response import OnboardResponse


class SequenceNumberService:
    """
    Service to generate sequence numbers while sending messages to the agrirouter. The sequence
    number generation is based on the ID of the endpoint, therefore a sequence number can be used
    multiple times for different endpoints.
    """
    sequence_numbers_for_endpoints: Dict[str, int] = {}

    @staticmethod
    def generate_sequence_number_for_endpoint(onboarding_response: OnboardResponse) -> int:
        """
        Generate sequence number for the onboarding response
        params: Onboard response
        returns: 1 if 1st call, 1+n if nth call
        """
        endpoint_id = onboarding_response.sensor_alternate_id
        SequenceNumberService.sequence_numbers_for_endpoints.setdefault(endpoint_id, 1)
        current_sequence_number = SequenceNumberService.sequence_numbers_for_endpoints[endpoint_id]
        SequenceNumberService.sequence_numbers_for_endpoints[endpoint_id] = current_sequence_number + 1
        return current_sequence_number
