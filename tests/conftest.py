import pytest
import hashlib
import pytest
import hashlib
from fastapi.testclient import TestClient
from planetmint_cryptoconditions.crypto import Ed25519SigningKey
from cid_resolver.main import app


def sign_challenge(challenge):
    SK_B58_ILP = b"9qLvREC54mhKYivr88VpckyVWdAFmifJpGjbvV5AiTRs"
    sk = Ed25519SigningKey(SK_B58_ILP)

    byte_string = bytes(challenge, "utf-8")
    hash_local = hashlib.sha256()
    hash_local.update(byte_string)

    signature = sk.sign(hash_local.digest())
    return signature


@pytest.fixture
def bearer_token():
    client = TestClient(app)
    VK_B58_ILP = b"Gtbi6WQDB6wUePiZm8aYs5XZ5pUqx9jMMLvRVHPESTjU"
    response = client.get(f"auth?public_key={VK_B58_ILP.decode()}")
    signature = sign_challenge(response.json()["challenge"])

    jwt_response = client.post(f"auth?public_key={VK_B58_ILP.decode()}&signature={signature.decode()}")
    return jwt_response.json()["access_token"]
