import time
import secrets
from cid_resolver.app.verify_signature import validate_signature_data_string
from cid_resolver.config import (
    AUTH_CHALLENGE_SIZE,
    AUTH_CHALLENGE_TIMEOUT_IN_SEC,
)

challenges = {}


def cleanup_pending_challenges():
    for key in list(challenges.keys()):
        if challenges[key][1] + AUTH_CHALLENGE_TIMEOUT_IN_SEC < time.time():
            del challenges[key]


def does_pub_key_belong_to_valid_actor(pub_key: str) -> bool:
    return True


def create_challenge(pub_key: str) -> int:
    cleanup_pending_challenges()
    challenges[pub_key] = (
        bytes([secrets.randbelow(256) for _ in range(0, AUTH_CHALLENGE_SIZE)]),
        time.time(),
    )
    return challenges[pub_key][0]


def verify_signed_challenge(pub_key: bytes, signature: str) -> bool:
    if pub_key not in challenges:
        return False
    return validate_signature_data_string(pub_key, signature, challenges[pub_key][0].hex())
