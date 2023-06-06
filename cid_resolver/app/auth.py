import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from datetime import datetime
from fastapi import status, HTTPException
import random
from pydantic import ValidationError
from cid_resolver.app.verify_signature import validate_signature_data_string
from cid_resolver.config import (
    AUTH_JWT_REFRESH_SECRET_KEY, 
    AUTH_JWT_SECRET_KEY, 
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES,
    AUTH_REFRESH_TOKEN_EXPIRE_MINUTES,
    AUTH_ALGORITHM,
    AUTH_CHALLENGE_SIZE,
    AUTH_CHALLENGE_TIMEOUT_IN_SEC )

challenges = {}


def get_timestamp_for_now():
    return datetime.timestamp(datetime.utcnow())

def cleanup_pending_challenges():
    for key in challenges:
        if challenges[key][1]+AUTH_CHALLENGE_TIMEOUT_IN_SEC < get_timestamp_for_now():
            del challenges[key]

def does_pub_key_belong_to_valid_actor(pub_key: str) -> bool:
    return True

def create_challenge( pub_key: str ) -> int:
    cleanup_pending_challenges()
    challenges[ pub_key ] = ( bytes([random.randint(0, 255) for _ in range(0, AUTH_CHALLENGE_SIZE)]), get_timestamp_for_now())
    return challenges[ pub_key ][0]
    

def verify_signed_challenge(pub_key: bytes, signature: str) -> bool:
    if pub_key not in challenges:
        return False
    return validate_signature_data_string( pub_key, signature, challenges[pub_key][0].hex() )
        
        

def create_access_token(public_key: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "public_key": str(public_key)}
    encoded_jwt = jwt.encode(to_encode, AUTH_JWT_SECRET_KEY, AUTH_ALGORITHM)
    return encoded_jwt

def create_refresh_token(public_key: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=AUTH_REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "public_key": str(public_key)}
    encoded_jwt = jwt.encode(to_encode, AUTH_JWT_REFRESH_SECRET_KEY, AUTH_ALGORITHM)
    return encoded_jwt

def verify_token( token: str )-> str:
    try:
        payload = jwt.decode(
            token, AUTH_JWT_SECRET_KEY, algorithms=[AUTH_ALGORITHM]
        )
        
        
        if datetime.fromtimestamp(payload['exp']) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload['public_key']
        
