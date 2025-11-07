# Research: Visual Sticky Notes Collaboration Platform

**Date**: 2025-11-07  
**Purpose**: Resolve technical unknowns and establish implementation approach

## Research Tasks Completed

### 1. Real-time Collaboration Architecture

**Decision**: WebSocket-based real-time updates with optimistic UI updates

**Rationale**: 
- WebSockets provide bidirectional communication for <200ms update requirements
- Optimistic updates improve perceived performance during network latency
- Event-driven architecture naturally supports multiple concurrent users
- Proven pattern for collaborative editing applications

**Alternatives considered**:
- Server-Sent Events: Unidirectional, would require separate HTTP for user actions
- Polling: Would not meet 200ms requirement, poor performance at scale
- WebRTC: Peer-to-peer adds complexity, requires fallback servers anyway

**Implementation approach**:
- FastAPI WebSocket endpoints for real-time events
- Redux/Vuex-style state management with optimistic updates
- Conflict resolution through last-writer-wins with timestamps
- Connection recovery with state synchronization

### 2. Canvas and Spatial Positioning

**Decision**: HTML5 Canvas with virtual coordinate system and viewport management

**Rationale**:
- Canvas provides infinite scrolling with viewport-based rendering
- Virtual coordinates allow precise positioning independent of screen size
- Hardware acceleration available for smooth dragging and zooming
- Export to image formats directly supported

**Alternatives considered**:
- SVG: Better for text editing but poor performance with 1000+ elements
- DOM manipulation: Infinite scroll difficult, poor performance at scale
- WebGL: Overkill for 2D positioning, adds complexity

**Implementation approach**:
- Canvas viewport management with pan/zoom
- Virtual coordinate system (-∞ to +∞)
- Spatial indexing for efficient collision detection
- Lazy rendering of off-screen notes

### 3. Export Generation Architecture

**Decision**: Backend-based export generation with headless browser for visual formats

**Rationale**:
- Server-side generation ensures consistent output across client devices
- Headless Chrome/Puppeteer for high-quality PDF and image generation
- Python libraries (reportlab, PIL) for structured data exports
- Asynchronous processing prevents UI blocking

**Alternatives considered**:
- Client-side export: Browser compatibility issues, performance problems
- Static image generation: Poor quality for spatial layouts
- Third-party services: Adds external dependency and privacy concerns

**Implementation approach**:
- Background job queue for export processing
- Template-based PDF generation preserving spatial relationships
- High-resolution canvas rendering for image exports
- Streaming downloads for large workspaces

### 4. Data Persistence and Backup Strategy

**Decision**: PostgreSQL with JSON columns for flexibility, Redis for real-time state, automated backup pipeline

**Rationale**:
- PostgreSQL provides ACID compliance for critical workspace data
- JSON columns allow flexible note metadata without schema changes
- Redis handles ephemeral real-time session state efficiently
- Automated backup meets 99.99% durability requirement

**Alternatives considered**:
- MongoDB: Less mature backup ecosystem, consistency concerns
- SQLite: Single-file simplicity but poor concurrency support
- In-memory only: Would not meet persistence requirements

**Implementation approach**:
- PostgreSQL for persistent data (workspaces, notes, users)
- Redis for active sessions and real-time state
- Continuous WAL-based backups to cloud storage
- Point-in-time recovery with 90-day retention

### 5. Authentication and Guest Access

**Decision**: JWT-based session tokens with optional user registration

**Rationale**:
- JWT tokens enable stateless authentication for horizontal scaling
- Guest access with optional names meets simplicity requirement
- No complex OAuth integration needed for MVP
- Easy to extend with social login later

**Alternatives considered**:
- Session cookies: Stateful, complicates horizontal scaling
- OAuth only: Adds complexity for guest access requirement
- No authentication: Cannot track workspace ownership/permissions

**Implementation approach**:
- Guest tokens with optional display names
- Workspace ownership tracking for data retention policies
- Facilitator permissions based on workspace creation
- Token refresh for long-running collaborative sessions

### 6. Template System Architecture

**Decision**: Configurable layout engines with constraint-based positioning

**Rationale**:
- Template patterns (Kanban, mind map) can be expressed as spatial constraints
- Constraint solver allows automatic organization while preserving manual overrides
- Extensible system for future template types
- Templates apply as layout guides, not rigid containers

**Alternatives considered**:
- Fixed grid systems: Too restrictive for creative layouts
- Manual positioning only: Users want familiar structures
- Complex layout engines: Violates simplicity principle

**Implementation approach**:
- Template definitions as JSON configuration
- Constraint-based auto-positioning with override capability
- Template preview before application
- Smooth transitions when applying/removing templates

## Technology Stack Finalized

### Frontend
- **Build Tool**: Vite 5.x (fast development, minimal configuration)
- **Framework**: Vanilla JavaScript + minimal libraries (maintains simplicity)
- **Real-time**: Native WebSocket API
- **Canvas**: HTML5 Canvas API with custom utilities
- **State**: Custom lightweight state management

### Backend  
- **Framework**: FastAPI 0.104+ (async support, automatic OpenAPI)
- **Database**: PostgreSQL 15+ (primary data storage)
- **Cache**: Redis 7+ (real-time session state)
- **WebSockets**: FastAPI WebSocket support
- **Export**: Puppeteer (PDF/image), Python libraries (JSON/CSV)
- **Background Jobs**: Celery + Redis (export processing)

### Infrastructure
- **Deployment**: Docker Compose (development), Kubernetes (production)
- **Database**: PostgreSQL with automated backups
- **File Storage**: Local development, cloud storage for production
- **Monitoring**: Built-in FastAPI metrics, database connection pooling

## Performance Optimizations Identified

1. **Canvas Rendering**: Viewport-based rendering, only draw visible notes
2. **WebSocket Efficiency**: Batch updates, compress repeated operations
3. **Database**: Connection pooling, prepared statements, spatial indexing
4. **Export Performance**: Async processing, result caching, incremental generation
5. **Real-time Scaling**: Redis pub/sub for multi-server deployments

## Security Considerations

1. **Input Validation**: Strict note content limits, XSS prevention
2. **Rate Limiting**: Per-user limits on note creation, export requests
3. **Data Isolation**: Workspace-level access controls
4. **Export Security**: Sanitize content before PDF/image generation
5. **Backup Security**: Encrypted backup storage, access audit logs