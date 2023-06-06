from fastapi import APIRouter, HTTPException
from fastapi.security.http import HTTPBearer
from cid_resolver.app.JWTBearer import JWTBearer

from cid_resolver.app.auth import verify_signed_challenge, create_challenge

router = APIRouter(
    prefix="/auth",
    tags=["EdDSA challenge-response authentication"],
    responses={404: {"detail": "Not found"}},
)

get_bearer_token = HTTPBearer(auto_error=False)


@router.get("/", summary="request a challenge that is to be signed and posted.")
async def get_challenge(public_key: str) -> str:
    challenge = create_challenge(public_key)
    return {"challenge": challenge.hex()}


@router.post("/", summary="Send the signed challenge to get access and refresh tokens.")
async def post_signed_challenge(public_key: str, signature: str) -> dict:
    if verify_signed_challenge(public_key, signature):
        response = JWTBearer.signJWT(public_key)
        return response
    else:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")
