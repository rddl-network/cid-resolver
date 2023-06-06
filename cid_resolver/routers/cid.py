from fastapi import APIRouter, HTTPException, Depends
from cid_resolver.config import REDIS_AUTH, REDIS_HOST, REDIS_PORT
from cid_resolver.routers.auth import verify_jwt_token
router = APIRouter(
    prefix="/entry",
    tags=["CID entries"],
    responses={404: {"detail": "Not found"}},
)

import redis

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_AUTH, db=0)
redis_client = redis.Redis(connection_pool=pool)


@router.get("/cid")
async def resolve_cid(cid: str):
    try:
        url = redis_client.get(cid)
        if not url:
            raise HTTPException(status_code=404, detail="Item not found.")
        return {"cid": cid, "url": url}
    except redis.exceptions.ConnectionError as e:
        raise HTTPException(status_code=420, detail=f"Connection to Redis server failed: {e}")

from cid_resolver.app.JWTBearer import JWTBearer
@router.post("/",  dependencies=[Depends(JWTBearer())])
async def register_cid(cid: str, url: str):
    try:
        redis_client.set(cid, url)
        return {}
    except redis.exceptions.ConnectionError as e:
        raise HTTPException(status_code=420, detail=f"Connection to Redis server failed: {e}")

