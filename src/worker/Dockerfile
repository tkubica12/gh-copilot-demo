FROM python:3.12-slim

RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

COPY pyproject.toml uv.lock .
RUN uv sync --frozen --no-dev

COPY main.py .

CMD ["uv", "run", "python", "main.py"]
