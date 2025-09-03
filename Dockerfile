FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY ./.python-version ./pyproject.toml ./uv.lock /app/

RUN uv sync --locked
COPY ./src /app/src/
COPY ./main.py /app/

ARG MILVUS_USERNAME
ARG MILVUS_PASSWORD
ARG OLLAMA_HOST

ENV MILVUS_USERNAME=$MILVUS_USERNAME
ENV MILVUS_PASSWORD=$MILVUS_PASSWORD
ENV OLLAMA_HOST=$OLLAMA_HOST

CMD ["uv", "run", "main.py"]