# Implementation Log

## 2025-09-01 – PDF Processing Feature Added

Implemented AI-enabled PDF processing capability extending the existing image processing pipeline to support PDF documents.

### Key Features Implemented
- **PDF File Support**: Extended API to accept PDF uploads alongside existing image types
- **Content Extraction**: Integrated markitdown library for robust PDF text extraction
- **AI Summarization**: PDF content is summarized using Azure OpenAI text completion API
- **Audit Logging**: Comprehensive logging throughout the processing pipeline for forensic purposes
- **Long-term Storage**: Original PDFs stored in Azure Blob Storage for compliance and forensic needs
- **Backward Compatibility**: All existing image processing functionality remains unchanged

### Technical Implementation

#### API Processing Service (`api-processing/`)
- Added file type validation for both images and PDFs
- Enhanced `/api/process` endpoint with proper HTTP status codes (400 for unsupported files)
- Extended message format with additional metadata (file_type, original_filename, timestamp)
- Implemented comprehensive audit logging for all processing steps

#### Worker Service (`worker/`)
- Added markitdown dependency for PDF content extraction
- Implemented PDF-specific processing pipeline with content extraction and summarization
- Enhanced message processing to handle both image and PDF files
- Added detailed audit logging and error handling for PDF processing

#### Testing
- Added comprehensive unit tests for PDF validation and processing logic
- Created integration tests validating message format and backward compatibility
- All existing tests continue to pass ensuring no regression
- Added worker-specific tests for PDF content extraction functionality

### Architecture Decisions
- **Reused Existing Infrastructure**: Leveraged existing Service Bus, Blob Storage, and Cosmos DB
- **Minimal Changes Principle**: Extended existing endpoints rather than creating new ones
- **Consistent Message Format**: Enhanced existing message structure with additional metadata
- **Error Handling**: Proper HTTP status codes and detailed error messages for unsupported files
- **Forensic Support**: Original files stored with metadata for compliance and audit requirements

### Dependencies Added
- `markitdown`: PDF content extraction library
- Enhanced logging throughout the pipeline
- UUID-based file naming for better organization

### Testing Coverage
- File type validation (PDF, images, unsupported formats)
- Content extraction and error handling
- Message format validation
- Backward compatibility verification
- End-to-end processing flow validation

## 2025-08-29 – Testing Infrastructure Added

Added unit and integration test scaffolding for `api-processing` and `api-status` services using `pytest`.

### Decisions
- Kept existing `requirements.txt` files; appended test dependencies via documentation instead of migrating to `pyproject.toml` to minimize scope. (A future improvement could consolidate dependency management under a single `pyproject.toml` per service in line with project guidelines.)
- Unit tests isolate business logic with faked Azure SDK clients (Blob, Service Bus, Cosmos) via fixtures in `tests/conftest.py`.
- Integration tests require explicit opt-in using `RUN_INTEGRATION_TESTS=1` and verify real interactions with Azure resources (Blob + Service Bus for processing API, Cosmos DB for status API).
- Adopted `integration` pytest marker; documented usage in READMEs.
 - Dynamic module loading added in tests to support hyphenated directory names (`api-processing`, `api-status`).

### Structure
```
api-processing/
  tests/
    unit/
    integration/
api-status/
  tests/
    unit/
    integration/
```

### Next Possible Improvements
- Introduce `pyproject.toml` + `uv` dependency groups (`[project.optional-dependencies].test`).
- Add GitHub Actions workflow to run unit tests on PR, with optional manual job for integration tests.
- Add more edge case coverage (invalid file types, Cosmos exceptions path, etc.).
- Add contract tests between processing & worker components once worker logic is available.

## 2025-08-29 – Migrated services to uv

Converted `api-processing` and `api-status` from `requirements.txt` + pip to `pyproject.toml` managed by `uv`.

### Changes
- Added `pyproject.toml` for each service with runtime dependencies and `test` optional dependency group.
- Removed legacy `requirements.txt` files.
- Updated READMEs to use `uv sync` and `uv run` commands; documented how to include test extras.
- Ensured existing test suite remains compatible (no code changes required).
 - Added dev dependency list mirroring test extras so `uv sync --dev` also installs test tooling.

### Rationale
Aligns with repository guidance to use `uv` for Python dependency management, improving reproducibility and enabling optional dependency groups.

## 2025-08-31 – Test env loading enhancement

Updated test `conftest.py` in both services to load environment variables from each service's `.env` file before applying fallback defaults. This allows running tests against real Azure resources by just configuring the `.env` without manually exporting variables, while still keeping deterministic defaults for unit tests.

## 2025-08-31 – Simplified integration test trigger

Removed reliance on `RUN_INTEGRATION_TESTS` environment flag. Integration tests are now included only when selected via the pytest marker (`-m integration`). Skips now occur solely on absence of required Azure environment variables. Documentation updated accordingly.

### 2025-08-31 – Integration test skip timing fix
Adjusted integration test modules to load `.env` before evaluating `@pytest.mark.skipif` so that environment variables defined only in the service `.env` file are recognized during collection. Previously the skip condition ran before the autouse fixture loaded `.env`, causing false skips.

