# Quickstart Guide: Visual Sticky Notes Platform

**Last Updated**: 2025-11-07  
**Target Audience**: Developers, Product Managers, QA Engineers

## Overview

The Visual Sticky Notes Collaboration Platform enables real-time collaborative brainstorming through digital sticky notes on an infinite canvas. This guide covers setup, core workflows, and key integration points.

## Architecture Summary

- **Frontend**: Vite + TypeScript, WebSocket client, HTML5 Canvas
- **Backend**: FastAPI + Python, PostgreSQL, Redis, WebSocket server
- **Real-time**: WebSocket-based collaboration with optimistic updates
- **Export**: Server-side generation (PDF, images, structured data)
- **Deployment**: Docker Compose (dev), Kubernetes (production)

## Quick Setup (Development)

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### 1. Clone and Initialize
```bash
git checkout 001-visual-sticky-notes
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

### 2. Start Services
```bash
docker-compose up -d postgres redis
cd backend && uvicorn src.main:app --reload --port 8000
cd frontend && npm run dev
```

### 3. Verify Setup
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Core User Workflows

### 1. Create Workspace
```bash
curl -X POST http://localhost:8000/api/v1/workspaces \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Team Brainstorm",
    "description": "Q4 Planning Session"
  }'
```

**Response**: Workspace ID and access details

### 2. Join Collaborative Session
1. Open workspace URL: `http://localhost:5173/workspace/{id}`
2. Enter optional display name
3. WebSocket connection established automatically
4. See other users' cursors and real-time changes

### 3. Create and Position Notes
1. Click "Add Note" or double-click canvas
2. Type content (max 5000 characters)
3. Drag to desired position
4. Changes sync to all users within 200ms

### 4. Apply Templates
1. Click "Templates" toolbar button
2. Select Kanban or Mind Map
3. Notes auto-organize with smooth animation
4. Manual repositioning still allowed

### 5. Export Results
1. Click "Export" in toolbar
2. Choose format: PDF, PNG/JPG, JSON, CSV
3. Background processing with download link
4. Files ready within 10 seconds for typical workspaces

## Key Integration Points

### WebSocket Connection
```javascript
const ws = new WebSocket(`ws://localhost:8000/api/v1/workspaces/${id}/session`);

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  switch (message.type) {
    case 'note_created':
      addNoteToCanvas(message.note);
      break;
    case 'user_joined':
      showUserCursor(message.user);
      break;
  }
};

// Send note creation
ws.send(JSON.stringify({
  type: 'note_create',
  note: {
    content: 'New idea',
    x_position: 100,
    y_position: 200
  }
}));
```

### REST API Usage
```python
import httpx

# Create workspace
response = httpx.post('http://localhost:8000/api/v1/workspaces', json={
    'name': 'API Test Workspace'
})
workspace_id = response.json()['id']

# Add note
httpx.post(f'http://localhost:8000/api/v1/workspaces/{workspace_id}/notes', json={
    'content': 'API created note',
    'x_position': 0,
    'y_position': 0
})

# Export workspace
export_job = httpx.post(f'http://localhost:8000/api/v1/workspaces/{workspace_id}/export', json={
    'format': 'pdf'
})
job_id = export_job.json()['job_id']
```

## Canvas Integration

### Coordinate System
- Virtual coordinates: -∞ to +∞
- Viewport manages visible area
- Position precision: floating point
- Auto-pan when dragging near edges

### Performance Optimization
```javascript
// Viewport-based rendering
function renderVisibleNotes(viewport) {
  const visibleNotes = notes.filter(note => 
    isInViewport(note, viewport)
  );
  
  canvas.clear();
  visibleNotes.forEach(renderNote);
}

// Spatial indexing for collision detection
const spatialIndex = new QuadTree(notes);
const nearbyNotes = spatialIndex.query(draggedNote.bounds);
```

## Data Management

### Storage Limits
- Max 1000 notes per workspace
- Max 50MB total content per workspace
- Max 5000 characters per note
- Validation enforced at API and WebSocket layers

### Persistence Strategy
- PostgreSQL: Persistent data (workspaces, notes, users)
- Redis: Active sessions, real-time state
- Automatic cleanup: Guest workspaces after 30 days

### Backup & Recovery  
- Continuous WAL-based backups
- 90-day retention period
- Point-in-time recovery capability
- 15-minute recovery SLA

## Testing Strategy

### Unit Tests
```bash
# Backend
cd backend && pytest tests/unit/

# Frontend  
cd frontend && npm run test:unit
```

### Integration Tests
```bash
# API contract tests
cd backend && pytest tests/contract/

# WebSocket tests
cd backend && pytest tests/integration/websocket/
```

### End-to-End Tests
```bash
# Full user workflows
npm run test:e2e

# Multi-user collaboration
npm run test:e2e -- --spec collaboration.spec.js
```

## Deployment

### Production Deployment
```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sticky-notes-backend
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: backend
        image: sticky-notes:backend-v1.0.0
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
```

### Environment Configuration
```bash
# .env.production
DATABASE_URL=postgresql://user:pass@db:5432/stickynotes
REDIS_URL=redis://redis:6379/0
JWT_SECRET_KEY=production-secret-key
EXPORT_STORAGE_PATH=/app/exports
BACKUP_ENABLED=true
```

## Performance Monitoring

### Key Metrics
- WebSocket connection count
- Real-time update latency (<200ms target)
- Export generation time (<10s target)
- Database query performance
- Canvas rendering frame rate (>30 FPS)

### Health Checks
```bash
# API health
curl http://localhost:8000/health

# Database connectivity  
curl http://localhost:8000/health/db

# Redis connectivity
curl http://localhost:8000/health/redis
```

## Troubleshooting

### Common Issues

**WebSocket Connection Fails**
- Check firewall settings
- Verify JWT token validity
- Confirm workspace exists

**Real-time Updates Slow**
- Monitor Redis connection
- Check network latency
- Verify WebSocket message rate limits

**Export Generation Fails**
- Check disk space for temporary files
- Verify Puppeteer browser installation
- Monitor background job queue

**Canvas Performance Issues**
- Reduce viewport rendering area
- Enable spatial indexing
- Check for memory leaks in note objects

### Debug Mode
```bash
# Backend debug mode
DEBUG=true uvicorn src.main:app --reload

# Frontend debug mode
VITE_DEBUG=true npm run dev

# WebSocket message logging
DEBUG_WEBSOCKET=true npm run dev
```

## API Documentation

- **OpenAPI Spec**: http://localhost:8000/docs
- **WebSocket Contract**: [websocket.md](./contracts/websocket.md)
- **Data Models**: [data-model.md](./data-model.md)

## Next Steps

1. **Development**: Follow task list in `tasks.md` (generated by `/speckit.tasks`)
2. **Testing**: Implement test scenarios from acceptance criteria
3. **Deployment**: Configure production environment
4. **Monitoring**: Set up observability dashboards

For detailed implementation guidance, see the full specification in `spec.md` and technical research in `research.md`.