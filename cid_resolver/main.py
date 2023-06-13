from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from cid_resolver.routers import auth, cid


app = FastAPI()
# https://fastapi.tiangolo.com/tutorial/cors/?h=%20cors#use-corsmiddleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# health endpoint for Kubernetes
@app.get("/")
def get_health():
    return Response(content="", status_code=200)


app.include_router(auth.router)
app.include_router(cid.router)
