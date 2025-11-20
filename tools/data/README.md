# Data Tools

Toy profile and trip itinerary data generator and management scripts.

## Contents

### Toy Profiles
- `toy_profiles.json` - AI-generated toy profiles
- `toy-images/` - Avatar images (256x256 JPEG)
- `toy-profile-generator/` - AI generator using Azure OpenAI
- Scripts: `check-toy-profiles.py`, `clean-toy-profiles.py`, `import-toy-profiles.py`

### Trip Itineraries
- `trips.json` - AI-generated trip itineraries with legs
- `trip-images/` - Gallery images (512x512 JPEG)
- `toy-trip-generator/` - AI trip and gallery generator using Azure OpenAI
- Scripts: `check-trip-profiles.py`, `clean-trip-profiles.py`, `import-trip-profiles.py`

## Quick Start

### 1. Generate Toy Profiles

```powershell
cd toy-profile-generator
# Configure .env first (see .env.example)
uv sync
uv run python main.py
```

### 2. Generate Trip Itineraries

```powershell
cd ../toy-trip-generator
# Configure .env first (see .env.example)
uv sync
uv run python main.py
```

### 3. Start Services (for import)

```powershell
# Terminal 1 - Toy Service
cd ../src/services/toy
uv run uvicorn main:app --reload --port 8001

# Terminal 2 - Trip Service
cd ../src/services/trip
uv run uvicorn main:app --reload --port 8002
```

### 4. Import to Services

```powershell
cd ../../../tools/data
uv sync

# Import toys
uv run python import-toy-profiles.py

# Import trips
uv run python import-trip-profiles.py
```

### 5. Verify Data

```powershell
uv run python check-toy-profiles.py
uv run python check-trip-profiles.py
```

## Scripts

### Toy Profile Management

```powershell
# Import toy profiles to service
uv run python import-toy-profiles.py

# Check imported toys
uv run python check-toy-profiles.py

# Clean all toys
uv run python clean-toy-profiles.py
```

### Trip Profile Management

```powershell
# Import trip profiles to service
uv run python import-trip-profiles.py

# Check imported trips
uv run python check-trip-profiles.py

# Clean all trips
uv run python clean-trip-profiles.py
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Service endpoints
TOY_SERVICE_URL=http://localhost:8001
TRIP_SERVICE_URL=http://localhost:8002

# Toy data files
TOY_PROFILES_JSON=toy_profiles.json
TOY_IMAGES_FOLDER=toy-images

# Trip data files
TRIP_PROFILES_JSON=trips.json
TRIP_IMAGES_FOLDER=trip-images
```

## Workflow

1. **Generate toy profiles** with avatars using `toy-profile-generator` (outputs toy_profiles.json)
2. **Generate trip itineraries** with gallery images using `toy-trip-generator` (reads toy_profiles.json, outputs trips.json)
3. **Import toys** to toy service using `import-toy-profiles.py` (requires running service)
4. **Import trips** to trip service using `import-trip-profiles.py` (requires running service)
5. **Verify** everything using check scripts

## Key Design

- **Generators are independent**: toy-trip-generator reads from toy_profiles.json, not the API
- **Import scripts need services**: Only the import scripts require running services
- **Incremental generation**: Both generators skip already-processed items
- **Stable toy IDs**: Trip generator creates consistent UUIDs based on toy names

## Admin Role Support

Both `clean-toy-profiles.py` and `clean-trip-profiles.py` will delete ALL items as authentication has been removed.
