# Data Model: Visual Sticky Notes Collaboration Platform

**Date**: 2025-11-07  
**Purpose**: Define entities, relationships, and data structure

## Core Entities

### Workspace
Primary container for collaborative sessions.

**Attributes**:
- `id`: UUID (primary key)
- `name`: String (255) - Display name for the workspace
- `description`: Text - Optional description
- `owner_token`: String (nullable) - JWT token of workspace creator
- `is_guest_workspace`: Boolean - True if created by guest user
- `created_at`: Timestamp
- `last_activity_at`: Timestamp - Updated on any workspace activity
- `expires_at`: Timestamp (nullable) - Expiration for guest workspaces (30 days)
- `template_id`: String (nullable) - Currently applied template
- `canvas_bounds`: JSON - Virtual canvas boundaries for optimization
- `settings`: JSON - Workspace-specific configuration

**Validation Rules**:
- Name must be 1-255 characters
- Guest workspaces automatically get expiration date (30 days from creation)
- Registered user workspaces have null expiration
- Canvas bounds updated automatically based on note positions

**Relationships**:
- Has many: StickyNotes (1:N)
- Has many: Sessions (1:N) 
- Has one: Template (1:1, optional)

### StickyNote
Individual idea containers with content and position.

**Attributes**:
- `id`: UUID (primary key)
- `workspace_id`: UUID (foreign key to Workspace)
- `content`: Text - Note text content (max 5000 characters)
- `x_position`: Float - X coordinate in virtual space
- `y_position`: Float - Y coordinate in virtual space
- `width`: Integer - Note width in pixels (default: 200)
- `height`: Integer - Note height in pixels (default: 150)
- `color`: String - Hex color code (default: #FFFF88)
- `author_name`: String (nullable) - Display name of creator
- `author_token`: String - JWT token of creator (for permissions)
- `created_at`: Timestamp
- `updated_at`: Timestamp
- `is_locked`: Boolean - Prevents editing (default: false)
- `z_index`: Integer - Stacking order for overlapping notes
- `metadata`: JSON - Additional note properties (tags, categories, etc.)

**Validation Rules**:
- Content cannot exceed 5000 characters
- Position coordinates must be finite numbers
- Width: 100-500 pixels, Height: 100-400 pixels
- Color must be valid hex code
- Z-index auto-assigned on creation (max + 1)

**Relationships**:
- Belongs to: Workspace (N:1)

### User
Represents both guest and registered users.

**Attributes**:
- `id`: UUID (primary key)
- `token`: String - JWT token (unique identifier)
- `display_name`: String (nullable) - Optional display name
- `is_guest`: Boolean - True for guest users
- `email`: String (nullable) - For registered users only
- `created_at`: Timestamp
- `last_active_at`: Timestamp

**Validation Rules**:
- Display name: 1-50 characters if provided
- Email required for non-guest users
- Token must be unique across all users

**Relationships**:
- Has many: StickyNotes (via author_token)
- Has many: Sessions (1:N)

### Template
Predefined layout patterns for organizing notes.

**Attributes**:
- `id`: String (primary key) - Template identifier (e.g., "kanban", "mindmap")
- `name`: String - Display name
- `description`: Text - Template description
- `config`: JSON - Layout rules and constraints
- `preview_image`: String (nullable) - Path to preview image
- `is_active`: Boolean - Whether template is available
- `created_at`: Timestamp

**Built-in Templates**:

1. **Kanban Board**:
   ```json
   {
     "type": "kanban",
     "columns": [
       {"id": "todo", "name": "To Do", "x": 0, "width": 300},
       {"id": "progress", "name": "In Progress", "x": 350, "width": 300},
       {"id": "done", "name": "Done", "x": 700, "width": 300}
     ],
     "auto_position": true,
     "snap_to_columns": true
   }
   ```

2. **Mind Map**:
   ```json
   {
     "type": "mindmap",
     "center_position": {"x": 0, "y": 0},
     "branch_angle": 45,
     "level_spacing": 200,
     "auto_arrange": true,
     "connection_lines": true
   }
   ```

**Relationships**:
- Used by: Workspaces (1:N)

### Session
Active user sessions in workspaces (stored in Redis).

**Attributes** (Redis Hash):
- `session_id`: String (primary key)
- `workspace_id`: UUID
- `user_token`: String
- `user_name`: String (nullable)
- `is_facilitator`: Boolean
- `cursor_position`: JSON - Last known cursor position
- `active_note_id`: UUID (nullable) - Currently editing note
- `connected_at`: Timestamp
- `last_heartbeat`: Timestamp

**TTL**: 30 minutes (auto-cleanup inactive sessions)

**Relationships**:
- Belongs to: Workspace (N:1)
- Belongs to: User (N:1)

## Database Schema (PostgreSQL)

```sql
-- Workspaces table
CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_token VARCHAR(512),
    is_guest_workspace BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    last_activity_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    template_id VARCHAR(50),
    canvas_bounds JSONB,
    settings JSONB DEFAULT '{}',
    
    CONSTRAINT valid_name_length CHECK (length(name) >= 1),
    CONSTRAINT guest_expiration CHECK (
        (is_guest_workspace = false AND expires_at IS NULL) OR
        (is_guest_workspace = true AND expires_at IS NOT NULL)
    )
);

-- Sticky notes table
CREATE TABLE sticky_notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    x_position FLOAT NOT NULL,
    y_position FLOAT NOT NULL,
    width INTEGER DEFAULT 200,
    height INTEGER DEFAULT 150,
    color VARCHAR(7) DEFAULT '#FFFF88',
    author_name VARCHAR(50),
    author_token VARCHAR(512) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_locked BOOLEAN DEFAULT false,
    z_index INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    
    CONSTRAINT valid_content_length CHECK (length(content) <= 5000),
    CONSTRAINT valid_dimensions CHECK (
        width BETWEEN 100 AND 500 AND 
        height BETWEEN 100 AND 400
    ),
    CONSTRAINT valid_color CHECK (color ~ '^#[0-9A-Fa-f]{6}$'),
    CONSTRAINT finite_position CHECK (
        x_position IS NOT NULL AND y_position IS NOT NULL AND
        x_position = x_position AND y_position = y_position  -- NaN check
    )
);

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token VARCHAR(512) UNIQUE NOT NULL,
    display_name VARCHAR(50),
    is_guest BOOLEAN DEFAULT true,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    last_active_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT email_required_for_registered CHECK (
        (is_guest = true) OR (is_guest = false AND email IS NOT NULL)
    ),
    CONSTRAINT valid_display_name CHECK (
        display_name IS NULL OR length(display_name) >= 1
    )
);

-- Templates table
CREATE TABLE templates (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    config JSONB NOT NULL,
    preview_image VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Indexes for Performance

```sql
-- Workspace queries
CREATE INDEX idx_workspaces_owner ON workspaces(owner_token);
CREATE INDEX idx_workspaces_activity ON workspaces(last_activity_at);
CREATE INDEX idx_workspaces_expiration ON workspaces(expires_at) WHERE expires_at IS NOT NULL;

-- Note queries
CREATE INDEX idx_notes_workspace ON sticky_notes(workspace_id);
CREATE INDEX idx_notes_author ON sticky_notes(author_token);
CREATE INDEX idx_notes_position ON sticky_notes(workspace_id, x_position, y_position);
CREATE INDEX idx_notes_updated ON sticky_notes(updated_at);

-- User queries
CREATE INDEX idx_users_token ON users(token);
CREATE INDEX idx_users_activity ON users(last_active_at);
```

## State Transitions

### Workspace Lifecycle
1. **Created** → Active collaborative workspace
2. **Active** → Ongoing user activity, last_activity_at updated
3. **Inactive** → No activity for extended period
4. **Expired** → Guest workspace past 30-day limit (marked for deletion)
5. **Deleted** → Removed from system (cascade to all notes)

### StickyNote Lifecycle
1. **Created** → New note added to workspace
2. **Editing** → User actively modifying content
3. **Updated** → Position or content changed
4. **Locked** → Temporarily locked by facilitator
5. **Deleted** → Removed from workspace

### Session Lifecycle (Redis)
1. **Connected** → User joins workspace
2. **Active** → Regular heartbeat and activity
3. **Idle** → No activity but connection maintained
4. **Disconnected** → User leaves or connection lost
5. **Expired** → TTL reached, automatically cleaned up

## Data Storage Estimates

**Per Workspace (at maximum capacity)**:
- 1000 notes × 5KB average = 5MB content
- Spatial coordinates and metadata: ~500KB
- Total per workspace: ~5.5MB

**System Capacity**:
- 100,000 workspaces × 5.5MB = 550GB primary storage
- Redis sessions: ~50MB active state
- Backup storage: 550GB × 90 days × compression = ~15TB

## Data Validation and Constraints

**Application-Level Validation**:
- Workspace note count ≤ 1000 notes
- Total workspace content ≤ 50MB
- Real-time validation during note creation/updates
- Import validation against limits before processing

**Database-Level Constraints**:
- Foreign key relationships ensure data integrity
- Check constraints prevent invalid data
- Unique constraints on critical identifiers
- NOT NULL constraints on required fields