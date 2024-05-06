from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

SIGNATURE_ALGORITHM = "SHA256withRSA"


class SignatureService:

    @staticmethod
    def create_signature(request_body: str, private_key: str) -> str:
        private_key_bytes = bytearray(private_key.encode('utf-8'))
        private_key_data = load_pem_private_key(private_key_bytes, None)
        signature = private_key_data.sign(
            request_body.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return SignatureService._to_hex(signature)

    @staticmethod
    def _to_hex(sign: bytes):
        return sign.hex()

    @staticmethod
    def verify_signature(request_body: str, signature: bytes, public_key: str) -> None:
        public_key_bytes = bytearray(public_key.encode('utf-8'))
        public_key_data = load_pem_public_key(public_key_bytes)
        public_key_data.verify(
            signature,
            request_body.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
