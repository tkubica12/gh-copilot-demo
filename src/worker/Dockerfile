FROM python:3.12-slim

WORKDIR /app

ENV UV_USE_IO_URING=0

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml .
RUN uv pip compile pyproject.toml -o requirements.txt && \
    uv pip install --system -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]
