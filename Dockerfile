FROM python:3.10
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install poetry
COPY . /app
RUN poetry install
CMD ["poetry", "run", "uvicorn", "cid_resolver.main:app", "--host", "0.0.0.0", "--port", "80"]
