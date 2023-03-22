from fastapi import FastAPI, HTTPException
from decouple import config


app = FastAPI()
import redis


REDIS_HOST = config("REDIS_HOST", "localhost")
REDIS_PORT = config("REDIS_PORT", 6379)
REDIS_AUTH = config("REDIS_AUTH")


pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_AUTH, db=0)
redis_client = redis.Redis(connection_pool=pool)


@app.get("/entry/cid")
async def resolve_cid(cid: str):
    try:
        url = redis_client.get(cid)
        if not url:
            raise HTTPException(status_code=404, detail="Item not found.")
        return {"cid": cid, "url": url}
    except redis.exceptions.ConnectionError as e:
        raise HTTPException(status_code=420, detail="Connection to Redis server failed: {e}")


@app.post("/entry")
async def register_cid(cid: str, url: str):
    try:
        redis_client.set(cid, url)
        return {}
    except redis.exceptions.ConnectionError as e:
        raise HTTPException(status_code=420, detail="Connection to Redis server failed: {e}")
