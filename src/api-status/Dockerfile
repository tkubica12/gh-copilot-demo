FROM python:3.12-slim
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml /app/

# Install dependencies using uv pip with native TLS
RUN uv pip install --native-tls --system -e .

# Copy the application code
COPY main.py /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
