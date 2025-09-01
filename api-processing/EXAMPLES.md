# Example API Usage

## PDF Processing Example

```bash
# Upload a PDF for processing
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@document.pdf" \
  -H "Content-Type: multipart/form-data"

# Response:
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "results_url": "https://api-status.example.com/123e4567-e89b-12d3-a456-426614174000",
  "file_type": "pdf"
}
```

## Image Processing Example

```bash
# Upload an image for processing (existing functionality)
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@image.jpg" \
  -H "Content-Type: multipart/form-data"

# Response:
{
  "id": "987f6543-e21b-43d2-b456-789012345678",
  "results_url": "https://api-status.example.com/987f6543-e21b-43d2-b456-789012345678",
  "file_type": "image"
}
```

## Error Handling Example

```bash
# Upload unsupported file type
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@document.txt" \
  -H "Content-Type: multipart/form-data"

# Response (400 Bad Request):
{
  "detail": "Unsupported file type: text/plain. Supported types: images (JPEG, PNG, GIF, BMP) and PDFs"
}
```

## Supported File Types

- **Images**: JPEG, PNG, GIF, BMP
- **Documents**: PDF

## Processing Features

### For PDFs:
- Content extraction using markitdown
- AI-powered summarization
- Original document storage for forensics

### For Images:
- AI-powered description using Azure OpenAI Vision
- Object and scene recognition
- Original image storage