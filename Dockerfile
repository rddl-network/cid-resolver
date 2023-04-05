FROM --platform=linux/amd64 python:3.10-slim AS base
FROM base AS builder

RUN apt-get update && apt-get -y upgrade
RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /usr/src/app
COPY ./cid_resolver /usr/src/app/cid_resolver
COPY ./poetry.lock /usr/src/app/poetry.lock
COPY ./pyproject.toml /usr/src/app/pyproject.toml
COPY ./redis.conf /usr/src/app/redis.conf

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

EXPOSE 8000:8000

RUN adduser --system --group nonroot
USER nonroot

CMD ["uvicorn", "cid_resolver.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "240", "--log-level=debug"]
