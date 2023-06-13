import jwt
import base64
from cid_resolver.config import AUTH_JWT_SECRET_KEY, AUTH_ALGORITHM


def test_secret_encoding():
    payload = {"actor": "6B3NgjZbL2mQTZNzitq1zoCZjgKrRA16KfPAbhWXYAaz@m2m.rddl.io", "exp": 4085016283}
    decoded_key = base64.b64decode(AUTH_JWT_SECRET_KEY).decode("utf-8")
    token = jwt.encode(payload, decoded_key, algorithm=AUTH_ALGORITHM)
    assert (
        token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY3RvciI6IjZCM05nalpiTDJtUVRaTnppdHExem9DWmpnS3JSQTE2S2ZQQWJoV1hZQWF6QG0ybS5yZGRsLmlvIiwiZXhwIjo0MDg1MDE2MjgzfQ.H8VMlR5qcZ1B_mn4oK7gMndit4kztEwPUDmMXecHep8"
    )
