FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY services/trip/pyproject.toml ./

# Install dependencies
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy application code
COPY services/trip/ .

# Expose port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
