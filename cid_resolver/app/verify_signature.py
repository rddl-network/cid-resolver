import hashlib
from planetmint_cryptoconditions.crypto import Ed25519VerifyingKey

def validate_signature_data_string(pub_key: str, signature: bytearray, data_string: str) -> bool:
    byte_string = bytes(data_string, "utf-8")
    hash_local = hashlib.sha256()
    hash_local.update(byte_string)
    result = validate_signature_data_hash(pub_key, signature, hash_local.digest())
    return result


def validate_signature_data_hash(public_key: str, signature: bytearray, message: bytes) -> bool:
    result = True
    try:
        Ed25519VerifyingKey(public_key).verify(message, signature=signature)
    except ValueError as e:
        result = False
    return result
