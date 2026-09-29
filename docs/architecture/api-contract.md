# API Contract — Proof of Concept

Agreed by Omar & Makar (2026-09-29). Must match `backend/main.py` and the demo exactly.

## POST /posts

Create a post.

**Request**
```json
{
  "author": "string, 1-100 chars, required",
  "content": "string, 1-1000 chars, required"
}
```

**Response — 201 Created**
```json
{
  "id": "uuid string",
  "author": "string",
  "content": "string",
  "created_at": "ISO 8601 UTC timestamp"
}
```

**Response — 422 Unprocessable Entity** (validation error, FastAPI/Pydantic v2 default shape)
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "content"],
      "msg": "Field required",
      "input": { "author": "Omar" }
    }
  ]
}
```

## GET /posts

List posts, newest first.

**Response — 200 OK**
```json
[
  {
    "id": "uuid string",
    "author": "string",
    "content": "string",
    "created_at": "ISO 8601 UTC timestamp"
  }
]
```

## GET /health

**Response — 200 OK**
```json
{ "status": "ok" }
```

## Notes
- No auth in the POC — `author` is free text, not a verified identity.
- No persistence — restarting the backend clears all posts.
- CORS is open (`*`) for local demo only, not a production setting.
