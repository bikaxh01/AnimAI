# Project APIs

This document outlines the available API endpoints for managing projects.

---

## 1. Create a Project

Creates a new project. The status of the project defaults to `pending`.

- **Endpoint:** `POST /api/v1/projects`
- **Content-Type:** `application/json`

### Request Body

| Field    | Type   | Required | Description                                      |
| -------- | ------ | -------- | ------------------------------------------------ |
| `prompt` | string | Yes      | The text prompt to generate the manim animation. |

**Example Request:**
```json
{
  "prompt": "Create an animation of a bouncing ball."
}
```

### Response

Returns the created project object.

- **Status Code:** `200 OK`

**Example Response:**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": null,
  "description": null,
  "code_file": null,
  "video_url": null,
  "prompt": "Create an animation of a bouncing ball.",
  "status": "pending",
  "created_at": "2026-06-27T11:40:00Z",
  "updated_at": "2026-06-27T11:40:00Z"
}
```

---

## 2. List Projects

Retrieves a list of all projects, excluding any projects that have a `failed` status. The list is sorted by the most recently created projects first.

- **Endpoint:** `GET /api/v1/projects`
- **Content-Type:** `application/json`

### Request Body

*(No body required)*

### Response

Returns a list of project objects.

- **Status Code:** `200 OK`

**Example Response:**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Bouncing Ball",
    "description": "A simple animation of a red bouncing ball.",
    "code_file": "bounce.py",
    "video_url": "https://example.com/videos/bounce.mp4",
    "prompt": "Create an animation of a bouncing ball.",
    "status": "completed",
    "created_at": "2026-06-27T11:40:00Z",
    "updated_at": "2026-06-27T11:45:00Z"
  },
  {
    "id": "1c7d3c94-3a05-4c01-8b2b-4d6d3d4b6a9c",
    "title": null,
    "description": null,
    "code_file": null,
    "video_url": null,
    "prompt": "Draw a fractal tree.",
    "status": "pending",
    "created_at": "2026-06-27T11:35:00Z",
    "updated_at": "2026-06-27T11:35:00Z"
  }
]
```

---

## 3. Get Project Details

Retrieves the details of a specific project by its UUID.

- **Endpoint:** `GET /api/v1/projects/{pid}`
- **Content-Type:** `application/json`

### Path Parameters

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `pid` | string (UUID) | Yes | The unique identifier of the project. |

### Request Body

*(No body required)*

### Response

Returns the project object.

- **Status Code:** `200 OK`

**Example Response:**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Bouncing Ball",
  "description": "A simple animation of a red bouncing ball.",
  "code_file": "bounce.py",
  "video_url": "https://example.com/videos/bounce.mp4",
  "prompt": "Create an animation of a bouncing ball.",
  "status": "completed",
  "created_at": "2026-06-27T11:40:00Z",
  "updated_at": "2026-06-27T11:45:00Z"
}
```

### Errors

- **Status Code:** `404 Not Found`
  - Returned if no project with the provided `pid` exists.

**Example Error Response:**
```json
{
  "detail": "Project not found"
}
```

---

## 4. Update Project

Updates specific fields of a project.

- **Endpoint:** `PATCH /api/v1/projects/{pid}`
- **Content-Type:** `application/json`

### Path Parameters

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `pid` | string (UUID) | Yes | The unique identifier of the project to update. |

### Request Body

You only need to include the fields you want to update.

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `title` | string | No | The new title of the project. |
| `description` | string | No | The new description of the project. |
| `code_file` | string | No | The path/reference to the generated code. |
| `video_url` | string | No | The URL of the generated animation video. |
| `status` | string | No | The new status of the project (e.g. `generating_code`, `completed`, `failed`). |

**Example Request:**
```json
{
  "status": "storyboarding",
  "title": "Bouncing Ball Setup"
}
```

### Response

Returns the updated project object.

- **Status Code:** `200 OK`

**Example Response:**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Bouncing Ball Setup",
  "description": null,
  "code_file": null,
  "video_url": null,
  "prompt": "Create an animation of a bouncing ball.",
  "status": "storyboarding",
  "created_at": "2026-06-27T11:40:00Z",
  "updated_at": "2026-06-27T11:46:00Z"
}
```

### Errors

- **Status Code:** `404 Not Found`
  - Returned if no project with the provided `pid` exists.
