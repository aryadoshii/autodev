# Priority Todo List API Documentation

## 1. Base URL and Versioning

**Base URL:** `https://api.priority-todo-list.com`
**Version:** v1

All endpoints are prefixed with `/api/v1/`

## 2. Authentication (JWT)

### How to Register

**Endpoint:** `POST /api/v1/auth/register`

**Description:** Creates a new user account

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Status Codes:**
- `201 Created` - User created successfully
- `400 Bad Request` - Invalid input data
- `409 Conflict` - User already exists

**curl Example:**
```bash
curl -X POST https://api.priority-todo-list.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securePassword123"
  }'
```

### How to Login

**Endpoint:** `POST /api/v1/auth/login`

**Description:** Authenticates user and returns JWT token

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Status Codes:**
- `200 OK` - Login successful
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Invalid credentials

**curl Example:**
```bash
curl -X POST https://api.priority-todo-list.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securePassword123"
  }'
```

### How to Use Tokens

**Authentication Header:** `Authorization: Bearer <your-jwt-token>`

**Example:**
```bash
curl -X GET https://api.priority-todo-list.com/api/v1/tasks \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 3. Endpoints

### Task Entity

#### List All Tasks

**Endpoint:** `GET /api/v1/tasks`

**Description:** Retrieves all tasks with pagination, filtering, and sorting options

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Number of items per page (default: 10, max: 100)
- `priority_id` (integer, optional): Filter by priority ID
- `completed` (boolean, optional): Filter by completion status
- `sort_by` (string, optional): Field to sort by (default: created_at)
- `order` (string, optional): Sort order (asc or desc, default: desc)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "Complete project proposal",
      "description": "Write and submit the quarterly project proposal",
      "priority_id": 2,
      "completed": false,
      "created_at": "2023-10-15T08:30:00Z",
      "updated_at": "2023-10-15T08:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "pages": 1
  }
}
```

**Status Codes:**
- `200 OK` - Success
- `401 Unauthorized` - Missing or invalid token

**curl Example:**
```bash
curl -X GET "https://api.priority-todo-list.com/api/v1/tasks?page=1&limit=5&priority_id=2&sort_by=title&order=asc" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Get Task by ID

**Endpoint:** `GET /api/v1/tasks/{id}`

**Description:** Retrieves a specific task by its ID

**Path Parameters:**
- `id` (integer): Task ID

**Response:**
```json
{
  "id": 1,
  "title": "Complete project proposal",
  "description": "Write and submit the quarterly project proposal",
  "priority_id": 2,
  "completed": false,
  "created_at": "2023-10-15T08:30:00Z",
  "updated_at": "2023-10-15T08:30:00Z"
}
```

**Status Codes:**
- `200 OK` - Success
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Task not found

**curl Example:**
```bash
curl -X GET https://api.priority-todo-list.com/api/v1/tasks/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Create Task

**Endpoint:** `POST /api/v1/tasks`

**Description:** Creates a new task

**Request Body:**
```json
{
  "title": "Complete project proposal",
  "description": "Write and submit the quarterly project proposal",
  "priority_id": 2
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete project proposal",
  "description": "Write and submit the quarterly project proposal",
  "priority_id": 2,
  "completed": false,
  "created_at": "2023-10-15T08:30:00Z",
  "updated_at": "2023-10-15T08:30:00Z"
}
```

**Status Codes:**
- `201 Created` - Task created successfully
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Priority ID does not exist

**curl Example:**
```bash
curl -X POST https://api.priority-todo-list.com/api/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "Complete project proposal",
    "description": "Write and submit the quarterly project proposal",
    "priority_id": 2
  }'
```

#### Update Task

**Endpoint:** `PUT /api/v1/tasks/{id}`

**Description:** Updates an existing task

**Path Parameters:**
- `id` (integer): Task ID

**Request Body:**
```json
{
  "title": "Complete project proposal - Updated",
  "description": "Write and submit the quarterly project proposal with updated requirements",
  "priority_id": 3,
  "completed": true
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete project proposal - Updated",
  "description": "Write and submit the quarterly project proposal with updated requirements",
  "priority_id": 3,
  "completed": true,
  "created_at": "2023-10-15T08:30:00Z",
  "updated_at": "2023-10-15T09:15:00Z"
}
```

**Status Codes:**
- `200 OK` - Task updated successfully
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Task or priority not found

**curl Example:**
```bash
curl -X PUT https://api.priority-todo-list.com/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "Complete project proposal - Updated",
    "description": "Write and submit the quarterly project proposal with updated requirements",
    "priority_id": 3,
    "completed": true
  }'
```

#### Delete Task

**Endpoint:** `DELETE /api/v1/tasks/{id}`

**Description:** Deletes a task by its ID

**Path Parameters:**
- `id` (integer): Task ID

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

**Status Codes:**
- `200 OK` - Task deleted successfully
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Task not found

**curl Example:**
```bash
curl -X DELETE https://api.priority-todo-list.com/api/v1/tasks/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Priority Entity

#### List All Priorities

**Endpoint:** `GET /api/v1/priorities`

**Description:** Retrieves all priorities

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Low",
      "color": "#90EE90",
      "created_at": "2023-10-15T08:30:00Z",
      "updated_at": "2023-10-15T08:30:00Z"
    },
    {
      "id": 2,
      "name": "Medium",
      "color": "#FFD700",
      "created_at": "2023-10-15T08:30:00Z",
      "updated_at": "2023-10-15T08:30:00Z"
    },
    {
      "id": 3,
      "name": "High",
      "color": "#FF6347",
      "created_at": "2023-10-15T08:30:00Z",
      "updated_at": "2023-10-15T08:30:00Z"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `401 Unauthorized` - Missing or invalid token

**curl Example:**
```bash
curl -X GET https://api.priority-todo-list.com/api/v1/priorities \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Get Priority by ID

**Endpoint:** `GET /api/v1/priorities/{id}`

**Description:** Retrieves a specific priority by its ID

**Path Parameters:**
- `id` (integer): Priority ID

**Response:**
```json
{
  "id": 2,
  "name": "Medium",
  "color": "#FFD700",
  "created_at": "2023-10-15T08:30:00Z",
  "updated_at": "2023-10-15T08:30:00Z"
}
```

**Status Codes:**
- `200 OK` - Success
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Priority not found

**curl Example:**
```bash
curl -X GET https://api.priority-todo-list.com/api/v1/priorities/2 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Create Priority

**Endpoint:** `POST /api/v1/priorities`

**Description:** Creates a new priority

**Request Body:**
```json
{
  "name": "Critical",
  "color": "#FF0000"
}
```

**Response:**
```json
{
  "id": 4,
  "name": "Critical",
  "color": "#FF0000",
  "created_at": "2023-10-15T09:30:00Z",
  "updated_at": "2023-10-15T09:30:00Z"
}
```

**Status Codes:**
- `201 Created` - Priority created successfully
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid token

**curl Example:**
```bash
curl -X POST https://api.priority-todo-list.com/api/v1/priorities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "name": "Critical",
    "color": "#FF0000"
  }'
```

#### Update Priority

**Endpoint:** `PUT /api/v1/priorities/{id}`

**Description:** Updates an existing priority

**Path Parameters:**
- `id` (integer): Priority ID

**Request Body:**
```json
{
  "name": "Urgent",
  "color": "#FF4500"
}
```

**Response:**
```json
{
  "id": 4,
  "name": "Urgent",
  "color": "#FF4500",
  "created_at": "2023-10-15T09:30:00Z",
  "updated_at": "2023-10-15T09:45:00Z"
}
```

**Status Codes:**
- `200 OK` - Priority updated successfully
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Priority not found

**curl Example:**
```bash
curl -X PUT https://api.priority-todo-list.com/api/v1/priorities/4 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "name": "Urgent",
    "color": "#FF4500"
  }'
```

#### Delete Priority

**Endpoint:** `DELETE /api/v1/priorities/{id}`

**Description:** Deletes a priority by its ID

**Path Parameters:**
- `id` (integer): Priority ID

**Response:**
```json
{
  "message": "Priority deleted successfully"
}
```

**Status Codes:**
- `200 OK` - Priority deleted successfully
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Priority not found
- `409 Conflict` - Priority is referenced by tasks

**curl Example:**
```bash
curl -X DELETE https://api.priority-todo-list.com/api/v1/priorities/4 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 4. Pagination, Filtering, Sorting

### Pagination Parameters

All list endpoints support pagination through query parameters:

- `page`: Current page number (default: 1)
- `limit`: Number of items per page (default: 10, max: 100)

**Example:**
```bash
curl -X GET "https://api.priority-todo-list.com/api/v1/tasks?page=2&limit=20" \
  -H "Authorization: Bearer <token>"
```

### Filtering Parameters

List endpoints support filtering:

- `priority_id`: Filter tasks by priority ID
- `completed`: Filter by completion status (true/false)

**Example:**
```bash
curl -X GET "https://api.priority-todo-list.com/api/v1/tasks?priority_id=2&completed=false" \
  -H "Authorization: Bearer <token>"
```

### Sorting Parameters

List endpoints support sorting:

- `sort_by`: Field to sort by (e.g., title, created_at)
- `order`: Sort order (asc or desc, default: desc)

**Example:**
```bash
curl -X GET "https://api.priority-todo-list.com/api/v1/tasks?sort_by=created_at&order=asc" \
  -H "Authorization: Bearer <token>"
```

## 5. Error Handling Examples

### Common Error Responses

**Invalid Token:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

**Validation Error:**
```json
{
  "error": "Bad Request",
  "message": "Validation failed",