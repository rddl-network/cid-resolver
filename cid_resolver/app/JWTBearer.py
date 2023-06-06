import jwt
import time
from typing import Dict
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from cid_resolver.config import AUTH_ACCESS_TOKEN_EXPIRE_MINUTES, AUTH_JWT_SECRET_KEY, AUTH_ALGORITHM   


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
        return {
            "access_token": token
        }
    
    @staticmethod
    def signJWT(public_key: str) -> Dict[str, str]:
        payload = {
            "public_key": public_key,
            "expires": time.time() + AUTH_ACCESS_TOKEN_EXPIRE_MINUTES
        }
        token = jwt.encode(payload, AUTH_JWT_SECRET_KEY, algorithm=AUTH_ALGORITHM)

        return JWTBearer.token_response(token)
    
    @staticmethod
    def decodeJWT(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, AUTH_JWT_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except:
            return {}