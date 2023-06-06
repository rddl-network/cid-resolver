import hashlib
from fastapi.testclient import TestClient
from planetmint_cryptoconditions.crypto import Ed25519SigningKey
from cid_resolver.main import app
from cid_resolver.app.auth import challenges
from cid_resolver.app.JWTBearer import JWTBearer
client = TestClient(app)

VK_HEX_ILP = b"ec172b93ad5e563bf4932c70e1245034c35467ef2efd4d64ebf819683467e2bf"  # noqa E501
VK_B64_ILP = b"7Bcrk61eVjv0kyxw4SRQNMNUZ+8u/U1k6/gZaDRn4r8="
VK_B58_ILP = b"Gtbi6WQDB6wUePiZm8aYs5XZ5pUqx9jMMLvRVHPESTjU"
VK_BYT_ILP = b"\xec\x17+\x93\xad^V;\xf4\x93,p\xe1$P4\xc3Tg\xef.\xfdMd\xeb\xf8\x19h4g\xe2\xbf"  # noqa E501


SK_HEX_ILP = b"833fe62409237b9d62ec77587520911e9a759cec1d19755b7da901b96dca3d42"  # noqa E501
SK_B64_ILP = b"gz/mJAkje51i7HdYdSCRHpp1nOwdGXVbfakBuW3KPUI="
SK_B58_ILP = b"9qLvREC54mhKYivr88VpckyVWdAFmifJpGjbvV5AiTRs"
SK_BYT_ILP = b"\x83?\xe6$\t#{\x9db\xecwXu \x91\x1e\x9au\x9c\xec\x1d\x19u[}\xa9\x01\xb9m\xca=B"  # noqa E501



def sign_challenge(challenge):
    sk = Ed25519SigningKey(SK_B58_ILP)
    
    byte_string = bytes(challenge, "utf-8")
    hash_local = hashlib.sha256()
    hash_local.update(byte_string)

    signature = sk.sign(hash_local.digest())
    return signature

def test_challenge_response_cycle():
    response = client.get(f"auth?public_key={VK_B58_ILP.decode()}")
    assert response.status_code == 200
    assert len(response.json()["challenge"]) == 256


    assert challenges[ VK_B58_ILP.decode() ][0].hex() == response.json()["challenge"]
    signature = sign_challenge( response.json()["challenge"] )
    
    jwt_response = client.post(f"auth?public_key={VK_B58_ILP.decode()}&signature={signature.decode()}")
    assert jwt_response.status_code == 200
    

    assert JWTBearer.decodeJWT( jwt_response.json()["access_token"])["public_key"] == VK_B58_ILP.decode()
    
