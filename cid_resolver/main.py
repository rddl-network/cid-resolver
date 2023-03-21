from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from decouple import config


app = FastAPI()
# https://fastapi.tiangolo.com/tutorial/cors/?h=%20cors#use-corsmiddleware
origins = [
    "https://explorer.rddl.io",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import redis


REDIS_HOST = config("REDIS_HOST", "localhost")
REDIS_PORT = config("REDIS_PORT", 6379)
REDIS_AUTH = config("REDIS_AUTH")


pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_AUTH, db=0)
redis_client = redis.Redis(connection_pool=pool)


# health endpoint for Kubernetes
@app.get("/")
def get_health():
    return Response(content="", status_code=200)


@app.get("/entry/cid")
async def resolve_cid(cid: str):
    try:
        url = redis_client.get(cid)
        if not url:
            raise HTTPException(status_code=404, detail="Item not found.")
        return {"cid": cid, "url": url}
    except redis.exceptions.ConnectionError as e:
        raise HTTPException(status_code=420, detail="Connection to Redis server failed.")


@app.post("/entry")
async def register_cid(cid: str, url: str):
    try:
        redis_client.set(cid, url)
        return {}
    except redis.exceptions.ConnectionError as e:
        raise HTTPException(status_code=420, detail="Connection to Redis server failed.")
