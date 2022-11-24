# CID-Resolver

The RDDL CID-Resolver can be execute by running

```
poetry install
export REDIS_HOST=<ip/hostname>
export REDIS_PORT=<port>
export REDIS_AUTH=<password>
poetry run uvicorn cid_resolver.main:app --host 0.0.0.0 --port 8000
```

The configuration can be done by environment variable or by defining the environment variables in the ```.env``` file. An example ```.env``` file can be found at ```env-example```. Please adjust the variables and copy the file to ```.env```.

A docker container is build and run by running the following commands
```
docker build -t cid-resolver .
docker run --env REDIS_HOST='<ip>' --env REDIS_AUTH='<password>' --env REDIS_PORT=<port> -d --name cid-resolver -p 80:80 cid-resolver
```
