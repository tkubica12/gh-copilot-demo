# WebSocket Contract: Real-time Collaboration

**Endpoint**: `ws://localhost:8000/api/v1/workspaces/{workspace_id}/session`  
**Protocol**: WebSocket with JSON message format  
**Authentication**: JWT token via query parameter or message header

## Connection Flow

1. **Establish Connection**
   ```
   GET /api/v1/workspaces/{workspace_id}/session
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Key: [key]
   Authorization: Bearer [jwt_token]
   ```

2. **Connection Response**
   ```json
   {
     "type": "connection_established",
     "session_id": "sess_123",
     "workspace_id": "workspace_456",
     "user_info": {
       "name": "John Doe",
       "is_facilitator": true
     },
     "active_users": [
       {
         "session_id": "sess_124",
         "name": "Jane Smith",
         "cursor_position": {"x": 100, "y": 200}
       }
     ]
   }
   ```

## Message Types

### Client → Server Messages

#### Join Workspace
```json
{
  "type": "join_workspace",
  "user_name": "John Doe",
  "cursor_position": {"x": 0, "y": 0}
}
```

#### Note Operations
```json
{
  "type": "note_create",
  "note": {
    "content": "New idea",
    "x_position": 100.5,
    "y_position": 200.0,
    "color": "#FFFF88"
  }
}
```

```json
{
  "type": "note_update",
  "note_id": "note_123",
  "changes": {
    "content": "Updated content",
    "x_position": 150.0,
    "y_position": 250.0
  }
}
```

```json
{
  "type": "note_delete",
  "note_id": "note_123"
}
```

#### Cursor Tracking
```json
{
  "type": "cursor_move",
  "position": {"x": 300, "y": 400}
}
```

#### Editing State
```json
{
  "type": "note_edit_start",
  "note_id": "note_123"
}
```

```json
{
  "type": "note_edit_end",
  "note_id": "note_123"
}
```

#### Template Operations
```json
{
  "type": "template_apply",
  "template_id": "kanban",
  "preserve_positions": false
}
```

#### Heartbeat
```json
{
  "type": "heartbeat",
  "timestamp": "2025-11-07T10:30:00Z"
}
```

### Server → Client Messages

#### User Presence Updates
```json
{
  "type": "user_joined",
  "user": {
    "session_id": "sess_125",
    "name": "Alice Johnson",
    "is_facilitator": false,
    "cursor_position": {"x": 0, "y": 0}
  }
}
```

```json
{
  "type": "user_left",
  "session_id": "sess_125"
}
```

```json
{
  "type": "cursor_update",
  "session_id": "sess_124",
  "position": {"x": 350, "y": 450}
}
```

#### Note Change Broadcasts
```json
{
  "type": "note_created",
  "note": {
    "id": "note_456",
    "content": "New idea",
    "x_position": 100.5,
    "y_position": 200.0,
    "author_name": "John Doe",
    "created_at": "2025-11-07T10:30:00Z"
  },
  "author_session_id": "sess_123"
}
```

```json
{
  "type": "note_updated",
  "note_id": "note_456",
  "changes": {
    "content": "Updated idea",
    "x_position": 150.0,
    "updated_at": "2025-11-07T10:31:00Z"
  },
  "author_session_id": "sess_123"
}
```

```json
{
  "type": "note_deleted",
  "note_id": "note_456",
  "author_session_id": "sess_123"
}
```

#### Editing State Broadcasts
```json
{
  "type": "note_edit_started",
  "note_id": "note_456",
  "editor_session_id": "sess_124",
  "editor_name": "Jane Smith"
}
```

```json
{
  "type": "note_edit_ended",
  "note_id": "note_456",
  "editor_session_id": "sess_124"
}
```

#### Template Change Broadcasts
```json
{
  "type": "template_applied",
  "template_id": "kanban",
  "note_updates": [
    {
      "note_id": "note_123",
      "x_position": 50,
      "y_position": 100
    },
    {
      "note_id": "note_456", 
      "x_position": 400,
      "y_position": 100
    }
  ],
  "applied_by_session_id": "sess_123"
}
```

#### System Messages
```json
{
  "type": "workspace_limit_warning",
  "message": "Approaching note limit (950/1000)",
  "current_count": 950,
  "limit": 1000
}
```

```json
{
  "type": "error",
  "error_code": "NOTE_LIMIT_EXCEEDED",
  "message": "Cannot create note: workspace limit of 1000 notes exceeded",
  "request_id": "req_789"
}
```

```json
{
  "type": "heartbeat_response",
  "timestamp": "2025-11-07T10:30:00Z"
}
```

## Connection Management

### Heartbeat Protocol
- Client sends heartbeat every 30 seconds
- Server responds with heartbeat_response
- Connection considered dead if no heartbeat for 90 seconds
- Automatic reconnection with state synchronization

### Reconnection Flow
```json
{
  "type": "reconnect",
  "last_sync_timestamp": "2025-11-07T10:29:45Z"
}
```

**Server Response:**
```json
{
  "type": "sync_update",
  "workspace_state": {
    "notes": [...],  // All notes modified since last_sync_timestamp
    "active_users": [...],
    "current_template": "kanban"
  }
}
```

### Error Handling
```json
{
  "type": "error",
  "error_code": "WORKSPACE_NOT_FOUND",
  "message": "Workspace does not exist or has been deleted",
  "reconnect": false
}
```

```json
{  
  "type": "error",
  "error_code": "INSUFFICIENT_PERMISSIONS",
  "message": "Only facilitators can apply templates",
  "request_id": "req_456"
}
```

## Rate Limiting

- **Note Operations**: 10 per second per user
- **Cursor Updates**: 30 per second per user  
- **Heartbeats**: 1 per 30 seconds (required)
- **Template Operations**: 1 per 10 seconds per user

Exceeding limits results in temporary message dropping with warning:
```json
{
  "type": "rate_limit_warning",
  "message": "Too many cursor updates, throttling enabled",
  "retry_after": 1000
}
```

## Message Ordering and Consistency

### Optimistic Updates
1. Client applies change locally immediately
2. Client sends message to server
3. Server validates and broadcasts to other clients
4. If server rejects, client reverts local change

### Conflict Resolution
- Last-writer-wins based on server timestamp
- Facilitator actions take precedence over regular users
- Template applications override individual note positions

### State Synchronization
- Full state sync on connection establishment
- Incremental updates during session
- Automatic sync on reconnection with timestamp-based delta

## Connection Lifecycle

1. **Connect** → WebSocket handshake
2. **Authenticate** → JWT validation
3. **Join** → Send join_workspace message
4. **Active** → Real-time collaboration
5. **Idle** → Heartbeat-only communication
6. **Disconnect** → Clean session cleanup
7. **Cleanup** → Remove from active users after 30s