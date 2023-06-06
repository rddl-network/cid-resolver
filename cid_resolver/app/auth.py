import time
from typing import Union, Any
from jose import jwt
from datetime import datetime
import random
from cid_resolver.app.verify_signature import validate_signature_data_string
from cid_resolver.config import (
    AUTH_JWT_REFRESH_SECRET_KEY,
    AUTH_JWT_SECRET_KEY,
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES,
    AUTH_REFRESH_TOKEN_EXPIRE_MINUTES,
    AUTH_ALGORITHM,
    AUTH_CHALLENGE_SIZE,
    AUTH_CHALLENGE_TIMEOUT_IN_SEC,
)

challenges = {}


def cleanup_pending_challenges():
    for key in challenges:
        if challenges[key][1] + AUTH_CHALLENGE_TIMEOUT_IN_SEC < time.time():
            del challenges[key]


def does_pub_key_belong_to_valid_actor(pub_key: str) -> bool:
    return True


def create_challenge(pub_key: str) -> int:
    cleanup_pending_challenges()
    challenges[pub_key] = (
        bytes([random.randint(0, 255) for _ in range(0, AUTH_CHALLENGE_SIZE)]),
        time.time(),
    )
    return challenges[pub_key][0]


def verify_signed_challenge(pub_key: bytes, signature: str) -> bool:
    if pub_key not in challenges:
        return False
    return validate_signature_data_string(pub_key, signature, challenges[pub_key][0].hex())
