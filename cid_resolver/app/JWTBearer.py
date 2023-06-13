import jwt
import time
import base64
from typing import Dict
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from cid_resolver.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET, JWT_ALGORITHM, JWT_DOMAIN


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not JWTBearer.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = JWTBearer.decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

    @staticmethod
    def token_response(token: str):
        return {"access_token": token}

    @staticmethod
    def _base64_decoded_secret() -> str:
        return base64.b64decode(JWT_SECRET).decode("utf-8")

    @staticmethod
    def signJWT(public_key: str) -> Dict[str, str]:
        payload = {"actor": f"{public_key}@{JWT_DOMAIN}", "exp": time.time() + JWT_ACCESS_TOKEN_EXPIRE_MINUTES}

        token = jwt.encode(payload, JWTBearer._base64_decoded_secret(), algorithm=JWT_ALGORITHM)

        return JWTBearer.token_response(token)

    @staticmethod
    def decodeJWT(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, JWTBearer._base64_decoded_secret(), algorithms=[JWT_ALGORITHM])
            return decoded_token if decoded_token["exp"] >= time.time() else None
        except:
            return {}
