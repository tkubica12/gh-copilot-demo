# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml /app/

# Install dependencies using uv pip with native TLS
RUN uv pip install --native-tls --system -e .

# Copy the application code
COPY main.py /app/

# Run main.py when the container launches
CMD ["python", "main.py"]
