# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy pyproject.toml first for dependency installation
COPY pyproject.toml /app/

# Install any needed packages specified in pyproject.toml
# Install dependencies directly to avoid build dependencies issues
RUN pip install --no-cache-dir \
    python-dotenv \
    azure-identity \
    azure-storage-blob \
    azure-servicebus \
    opentelemetry-api \
    opentelemetry-sdk \
    azure-monitor-opentelemetry \
    azure-core-tracing-opentelemetry \
    opentelemetry-instrumentation-fastapi \
    opentelemetry-instrumentation-requests \
    opentelemetry-instrumentation-openai-v2 \
    openai \
    azure-cosmos \
    aiohttp

# Copy the current directory contents into the container at /app
COPY . /app

# Run main.py when the container launches
CMD ["python", "main.py"]
