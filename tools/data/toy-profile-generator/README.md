# Data generator: toy profiles

AI-powered toy profile and avatar generator using Azure OpenAI.

## Overview

Generates realistic toy profiles with:
- **AI-generated names** (short, catchy, memorable)
- **Funny descriptions** (cute, playful personality)
- **Avatar images** (1024x1024 generated, resized to 256x256 JPEG)
- **Owner assignment** (randomly distributed across provided OIDs)

Uses GPT-4o for text generation with structured outputs and gpt-image-1 for image generation, authenticated via `DefaultAzureCredential`.

## Setup

1. **Install dependencies:**
   ```powershell
   uv sync
   ```

2. **Configure environment:**
   Copy `.env.example` to `.env` and populate with your Azure AI Foundry values:
   ```powershell
   copy .env.example .env
   ```

   Required configuration:
   - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint (e.g., `https://your-resource.openai.azure.com/openai/v1/`)
   - `GPT_DEPLOYMENT_NAME`: Your GPT model deployment name (e.g., `gpt-4o`)
   - `IMAGE_DEPLOYMENT_NAME`: Your image model deployment name (e.g., `gpt-image-1`)
   - `NUM_TOYS`: Number of profiles to generate (e.g., `10`)
   - `OWNER_OIDS`: Comma-separated list of Entra object IDs (e.g., `12345678-...,87654321-...`)

3. **Authenticate:**
   Ensure you're logged in with Azure CLI or have appropriate credentials:
   ```powershell
   az login
   ```

## Usage

Run the generator:
```powershell
uv run main.py
```

### Output

- **JSON data:** `toy_profiles.json` in current directory
  - Array of objects with: `id`, `owner_oid`, `name`, `description`, `avatar_blob_name`
- **Images:** `../toy-images/*.jpg` (UUID-named JPEG files, 256x256px)

### Example Output

```json
[
  {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "owner_oid": "12345678-1234-1234-1234-123456789012",
    "name": "Captain Whiskers",
    "description": "A dashing pirate cat with a tiny tricorn hat...",
    "avatar_blob_name": "a3f8e9d2-7c4b-4e1f-9a8d-2c5b6e3f7a9d.jpg"
  }
]
```

## Features

- **Structured outputs** for reliable parsing
- **Duplicate prevention** by feeding previous toys into prompts
- **Progress tracking** with emoji indicators
- **Error handling** with helpful messages
- **Optimized images** (JPEG quality 85, optimized compression)
- **Secure auth** via DefaultAzureCredential (no API keys)