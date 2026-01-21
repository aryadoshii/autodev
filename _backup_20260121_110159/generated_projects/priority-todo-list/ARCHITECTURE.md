# Priority Todo List - Architecture Documentation

## 1. System Overview

### High-Level Architecture Diagram

```mermaid
graph TD
    subgraph "Frontend"
        A[React Web App] --> B[API Gateway]
    end
    
    subgraph "Backend"
        B --> C[FastAPI Server]
        C --> D[Authentication Service]
        C --> E[Todo Service]
        C --> F[User Service]
        C --> G[Database]
    end
    
    subgraph "Infrastructure"
        H[Docker Containers]
        I[Load Balancer]
        J[Reverse Proxy]
    end
    
    A --> H
    C --> H
    G --> H
    H --> I
    I --> J
    J --> A
```

### Component Interaction

The system follows a client-server architecture with clear separation of concerns:

1. **Frontend** (React) - User interface that communicates with the backend via REST API
2. **Backend** (FastAPI) - Handles business logic, authentication, and data processing
3. **Database** (PostgreSQL) - Persistent storage for user and todo data
4. **Infrastructure** - Containerization and deployment orchestration

## 2. Backend Architecture

### Directory Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── todos.py
│   │   │   └── users.py
│   │   └── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/
│   │   ├── base.py
│   │   ├── user.py
│   │   └── todo.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── todo.py
│   │   └── user.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── todo_service.py
│   │   └── user_service.py
│   └── utils/
│       └── helpers.py
├── tests/
├── requirements.txt
└── Dockerfile
```

### Layer Separation

#### Routes Layer
Handles HTTP requests and responses, validates input, and delegates to services.

```python
# Example route structure
from fastapi import APIRouter, Depends
from ..services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/")
async def get_todos(current_user: User = Depends(get_current_user)):
    return await TodoService.get_all(current_user.id)
```

#### Services Layer
Contains business logic and coordinates between models and external services.

```python
# Example service structure
class TodoService:
    @staticmethod
    async def get_all(user_id: int):
        # Business logic here
        return await TodoRepository.get_all_by_user(user_id)
```

#### Models Layer
ORM definitions for database entities using SQLAlchemy.

```python
# Example model structure
class Todo(Base):
    __tablename__ = "todos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    priority: Mapped[int] = mapped_column(Integer)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant AuthController
    participant AuthService
    participant DB
    
    Client->>AuthController: POST /auth/login
    AuthController->>AuthService: Validate credentials
    AuthService->>DB: Check user credentials
    DB-->>AuthService: Return user data
    AuthService->>AuthController: Generate JWT token
    AuthController-->>Client: Return access_token
```

### Database Design

The backend uses PostgreSQL with the following schema:

- **Users table**: Stores user information
- **Todos table**: Stores todo items with priority levels
- **Relationships**: One-to-many between users and todos

## 3. Frontend Architecture

### Directory Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   ├── todos/
│   │   └── layout/
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   └── Dashboard.jsx
│   ├── services/
│   │   ├── api.js
│   │   └── authService.js
│   ├── store/
│   │   ├── index.js
│   │   └── todoSlice.js
│   ├── hooks/
│   │   └── useAuth.js
│   ├── routes/
│   │   └── ProtectedRoute.jsx
│   ├── utils/
│   │   └── helpers.js
│   └── App.jsx
├── public/
└── package.json
```

### Component Hierarchy

```mermaid
graph TD
    A[App] --> B[Layout]
    B --> C[Header]
    B --> D[Main Content]
    D --> E[ProtectedRoute]
    E --> F[Dashboard]
    F --> G[TodoList]
    G --> H[TodoItem]
    F --> I[AddTodoForm]
    F --> J[PriorityFilter]
```

### State Management

Uses Redux Toolkit for global state management:

```javascript
// Example slice structure
const todoSlice = createSlice({
  name: 'todos',
  initialState: {
    items: [],
    loading: false,
    error: null
  },
  reducers: {
    setTodos: (state, action) => {
      state.items = action.payload;
    }
  }
});
```

### Routing

```javascript
// Example routing structure
<BrowserRouter>
  <Routes>
    <Route path="/login" element={<Login />} />
    <Route path="/register" element={<Register />} />
    <Route path="/dashboard" element={
      <ProtectedRoute>
        <Dashboard />
      </ProtectedRoute>
    } />
  </Routes>
</BrowserRouter>
```

## 4. Data Flow

### Request/Response Cycle

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant DB
    
    Client->>API: HTTP Request
    API->>Service: Process request
    Service->>DB: Query/Update data
    DB-->>Service: Return data
    Service-->>API: Return response
    API-->>Client: HTTP Response
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant AuthService
    
    User->>Frontend: Submit login form
    Frontend->>Backend: POST /auth/login
    Backend->>AuthService: Verify credentials
    AuthService->>Backend: Return JWT token
    Backend-->>Frontend: Return token
    Frontend->>Backend: Include token in headers
    Backend->>Backend: Validate token
    Backend-->>User: Authorized access
```

### CRUD Operations Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Service
    participant DB
    
    User->>Frontend: Create todo
    Frontend->>API: POST /todos
    API->>Service: Create todo
    Service->>DB: Insert todo
    DB-->>Service: Return created todo
    Service-->>API: Return created todo
    API-->>Frontend: Return created todo
    Frontend-->>User: Display new todo
    
    User->>Frontend: Update todo
    Frontend->>API: PUT /todos/{id}
    API->>Service: Update todo
    Service->>DB: Update todo
    DB-->>Service: Return updated todo
    Service-->>API: Return updated todo
    API-->>Frontend: Return updated todo
    Frontend-->>User: Display updated todo
    
    User->>Frontend: Delete todo
    Frontend->>API: DELETE /todos/{id}
    API->>Service: Delete todo
    Service->>DB: Delete todo
    DB-->>Service: Confirm deletion
    Service-->>API: Return success
    API-->>Frontend: Return success
    Frontend-->>User: Remove todo from list
```

## 5. Database Schema

### Entity Relationship Diagram

```mermaid
erDiagram
    USER {
        integer id PK
        string email
        string hashed_password
        string full_name
        datetime created_at
        datetime updated_at
    }
    
    TODO {
        integer id PK
        string title
        text description
        integer priority
        boolean completed
        integer user_id FK
        datetime created_at
        datetime updated_at
    }
    
    USER ||--o{ TODO : "owns"
```

### Table Descriptions

#### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| email | VARCHAR(255) | Unique user email |
| hashed_password | TEXT | Password hash |
| full_name | VARCHAR(255) | User's full name |
| created_at | TIMESTAMP | Account creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

#### Todos Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| title | VARCHAR(200) | Todo title |
| description | TEXT | Detailed description |
| priority | INTEGER | Priority level (1-5) |
| completed | BOOLEAN | Completion status |
| user_id | INTEGER | Foreign key to users |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

## 6. Security

### Authentication Mechanism

- **JWT Tokens**: Secure token-based authentication
- **Password Hashing**: BCrypt hashing for password security
- **Token Expiration**: Access tokens expire after 1 hour
- **Refresh Tokens**: Long-lived refresh tokens for seamless re-authentication

### Authorization

- **Role-based Access Control**: Basic role system (user/admin)
- **Resource Ownership**: Users can only access their own todos
- **Middleware Protection**: Route protection middleware
- **Input Validation**: Strict validation on all endpoints

### Data Validation

```python
# Pydantic model validation example
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: int = Field(..., ge=1, le=5)
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v
```

## 7. Deployment Architecture

### Docker Containers

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/todo_db
    depends_on:
      - db
      
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
      
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=todo_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
volumes:
  postgres_data:
```

### Services Communication

```mermaid
graph LR
    A[Frontend] --> B[Backend API]
    B --> C[PostgreSQL]
    B --> D[Redis Cache] (Optional)
    B --> E[External Services] (Optional)
```

### Environment Configuration

#### Environment Variables

```bash
# .env file
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

#### Production Configuration

- **Load Balancing**: Nginx or cloud load balancer
- **Reverse Proxy**: HTTPS termination
- **Health Checks**: Liveness/readiness probes
- **Logging**: Centralized logging with structured format
- **Monitoring**: Prometheus metrics and Grafana dashboards
- **Backup Strategy**: Regular database backups
- **Auto-scaling**: Horizontal scaling based on demand

This architecture provides a scalable, secure, and maintainable foundation for the Priority Todo List application with clear separation of concerns and robust security measures.