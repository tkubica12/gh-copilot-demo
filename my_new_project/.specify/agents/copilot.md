# Visual Sticky Notes Platform Development Guidelines

Auto-generated from feature plans. Last updated: 2025-11-07

## Active Technologies

### Backend Stack
- **Python 3.11+**: FastAPI framework for REST APIs and WebSocket endpoints
- **FastAPI 0.104+**: Async web framework with automatic OpenAPI documentation
- **PostgreSQL 15+**: Primary database for persistent data storage
- **Redis 7+**: Session state management and real-time collaboration cache
- **SQLAlchemy**: ORM for database models and migrations
- **Celery + Redis**: Background job processing for export generation
- **Puppeteer**: Headless browser for PDF and image export generation
- **Pytest**: Unit, integration, and contract testing framework

### Frontend Stack
- **Vite 5.x**: Build tool and development server with fast HMR
- **TypeScript/JavaScript**: Frontend language with optional type checking
- **HTML5 Canvas API**: 2D rendering for infinite canvas and note positioning
- **WebSocket API**: Native browser WebSocket for real-time collaboration
- **Vanilla JavaScript**: Minimal library approach for simplicity and speed

### Infrastructure
- **Docker Compose**: Development environment containerization
- **Kubernetes**: Production deployment and orchestration
- **Nginx**: Reverse proxy and static file serving
- **Docker**: Application containerization

## Project Structure

```text
backend/
├── src/
│   ├── models/          # SQLAlchemy models (workspace, note, user, template)
│   ├── services/        # Business logic (collaboration, export, templates)
│   ├── api/            # FastAPI routes and WebSocket handlers
│   └── utils/          # Helper functions (export generators, validation)
├── tests/
│   ├── unit/           # Model and service tests
│   ├── integration/    # API endpoint tests
│   └── contract/       # API contract validation
├── migrations/         # Database schema migrations
└── requirements.txt    # Python dependencies

frontend/
├── src/
│   ├── components/     # UI components (StickyNote, Canvas, Toolbar)
│   ├── pages/          # Workspace views (main canvas, export dialog)
│   ├── services/       # API client, WebSocket manager, state management
│   └── utils/          # Canvas utilities, export helpers
├── tests/
│   ├── unit/           # Component tests
│   ├── integration/    # User flow tests
│   └── e2e/           # Full application tests
├── public/             # Static assets
├── package.json        # Frontend dependencies
└── vite.config.js     # Vite configuration

docker/
├── docker-compose.yml  # Development environment
├── Dockerfile.backend  # Python backend container
└── Dockerfile.frontend # Vite frontend container
```

## FastAPI Commands

### Development Server
```bash
# Start development server with hot reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Debug mode with verbose logging
DEBUG=true uvicorn src.main:app --reload --log-level debug
```

### Database Management
```bash
# Create new migration
alembic revision --autogenerate -m "Add workspace table"

# Apply migrations
alembic upgrade head

# Reset database (development only)
alembic downgrade base && alembic upgrade head
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test types
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/
```

## Vite Commands

### Development
```bash
# Start development server
npm run dev

# Start with specific port
npm run dev -- --port 3000

# Build for production
npm run build

# Preview production build
npm run preview
```

### Testing
```bash
# Run unit tests
npm run test:unit

# Run integration tests  
npm run test:integration

# Run E2E tests
npm run test:e2e

# Watch mode for development
npm run test:unit -- --watch
```

## PostgreSQL Schema

### Key Tables
```sql
-- Primary entities
CREATE TABLE workspaces (id UUID PRIMARY KEY, name VARCHAR(255), ...);
CREATE TABLE sticky_notes (id UUID PRIMARY KEY, workspace_id UUID, content TEXT, ...);
CREATE TABLE users (id UUID PRIMARY KEY, token VARCHAR(512), ...);
CREATE TABLE templates (id VARCHAR(50) PRIMARY KEY, name VARCHAR(100), ...);

-- Performance indexes
CREATE INDEX idx_notes_workspace ON sticky_notes(workspace_id);
CREATE INDEX idx_notes_position ON sticky_notes(workspace_id, x_position, y_position);
```

## WebSocket Implementation

### Connection Pattern
```python
# FastAPI WebSocket endpoint
@app.websocket("/api/v1/workspaces/{workspace_id}/session")
async def websocket_endpoint(websocket: WebSocket, workspace_id: str):
    await websocket.accept()
    # Handle real-time collaboration messages
```

### Client Integration
```javascript
// WebSocket connection management
const ws = new WebSocket(`ws://localhost:8000/api/v1/workspaces/${id}/session`);
ws.onmessage = handleRealtimeUpdate;
ws.send(JSON.stringify({type: 'note_create', note: {...}}));
```

## Canvas Development

### Performance Patterns
```javascript
// Viewport-based rendering for large workspaces
function renderVisibleNotes(viewport) {
  const visibleNotes = spatialIndex.query(viewport);
  canvas.clear();
  visibleNotes.forEach(renderNote);
}

// Optimistic updates for responsiveness
function createNoteOptimistic(note) {
  addNoteToCanvas(note);  // Immediate UI update
  websocket.send({type: 'note_create', note});  // Server sync
}
```

## Code Style

### Python (Backend)
- **PEP 8**: Standard Python style guide
- **FastAPI Patterns**: Use dependency injection for database sessions
- **Async/Await**: Use async functions for I/O operations
- **Type Hints**: Required for all function parameters and return values
- **Pydantic Models**: Use for request/response validation

```python
# Example FastAPI route
@router.post("/workspaces", response_model=WorkspaceResponse)
async def create_workspace(
    workspace: CreateWorkspaceRequest,
    db: AsyncSession = Depends(get_db)
) -> WorkspaceResponse:
    # Implementation
```

### TypeScript/JavaScript (Frontend)
- **ESLint + Prettier**: Automated formatting and linting
- **Functional Style**: Prefer pure functions and immutable data
- **ES6+ Features**: Use modern JavaScript syntax
- **Clear Naming**: Descriptive variable and function names
- **Canvas Patterns**: Separate rendering from state management

```javascript
// Example canvas component
class StickyNoteCanvas {
  constructor(containerId) {
    this.canvas = document.getElementById(containerId);
    this.ctx = this.canvas.getContext('2d');
  }
  
  renderNote(note) {
    // Canvas rendering logic
  }
}
```

## Recent Changes

### Feature 001: Visual Sticky Notes Platform (2025-11-07)
- **Added**: Complete collaborative sticky notes platform architecture
- **Technologies**: FastAPI + Vite stack with WebSocket real-time collaboration
- **Key Features**: Infinite canvas, template organization, comprehensive export/import
- **Database**: PostgreSQL with Redis for real-time state management

<!-- MANUAL ADDITIONS START -->
<!-- Add any manual customizations here - they will be preserved during updates -->
<!-- MANUAL ADDITIONS END -->