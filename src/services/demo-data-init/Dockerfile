FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Install uv for reproducible builds
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency metadata
COPY src/services/demo-data-init/pyproject.toml ./

RUN uv pip install --system --no-cache -r pyproject.toml

# Copy shared auth module so FastAPI service can import it
COPY src/shared/auth /app/auth

# Copy service source
COPY src/services/demo-data-init/ ./

# Bundle dataset assets inside the container
COPY tools/data/ /app/data/
ENV DEMO_DATA_ASSETS_PATH=/app/data

EXPOSE 8010

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8010/health || exit 1

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]
