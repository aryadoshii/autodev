"""Backend Developer Agent"""
import sys
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class BackendDeveloperAgent:
    """
    Agent responsible for:
    - Creating FastAPI application structure
    - Generating REST API endpoints (CRUD)
    - Implementing JWT authentication
    - Adding request/response validation
    - Business logic and error handling
    """
    
    def __init__(self, qwen_client):
        self.qwen_client = qwen_client
    
    async def generate_backend(self, pm_spec: Dict, db_schema: Dict) -> Dict:
        """
        Generate complete FastAPI backend
        
        Args:
            pm_spec: Product Manager specification
            db_schema: Database schema from DB Architect
        
        Returns:
            Dict with all backend files (main.py, routes, schemas, etc.)
        """
        logger.info("Starting backend generation...")
        
        # Generate different components
        backend = {
            "main_app": await self._generate_main_app(pm_spec),
            "auth": await self._generate_auth_system(pm_spec, db_schema),
            "routes": await self._generate_routes(pm_spec, db_schema),
            "schemas": await self._generate_schemas(db_schema),
            "dependencies": await self._generate_dependencies(pm_spec),
            "config": await self._generate_config()
        }
        
        logger.success(f"Backend generated with {len(backend['routes'])} route files")
        return backend
    
    async def _generate_main_app(self, pm_spec: Dict) -> str:
        """Generate main FastAPI application file"""
        
        app_name = pm_spec.get('app_name', 'app')
        description = pm_spec.get('description', 'API')
        
        prompt = f"""
Create a FastAPI main.py file for: {app_name}

Description: {description}

Requirements:
1. Initialize FastAPI app with proper configuration
2. Add CORS middleware
3. Include all routers (auth, users, tasks, etc.)
4. Add exception handlers
5. Include health check endpoint
6. Add startup/shutdown events
7. Configure logging

Generate complete, production-ready code with:
- Proper imports
- Error handling
- Documentation
- Best practices

Output the complete main.py file code.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            system_prompt="You are an expert FastAPI developer. Generate clean, production-ready code.",
            temperature=0.2,
            max_tokens=2000
        )
        
        return self._extract_code(code)
    
    async def _generate_auth_system(self, pm_spec: Dict, db_schema: Dict) -> str:
        """Generate JWT authentication system"""
        
        prompt = """
Create a complete JWT authentication system for FastAPI.

Requirements:
1. User registration endpoint (POST /auth/register)
2. Login endpoint (POST /auth/login) - returns JWT token
3. Token refresh endpoint (POST /auth/refresh)
4. Password hashing with bcrypt
5. JWT token generation and validation
6. Dependencies for protected routes (get_current_user)

Include:
- Pydantic schemas for request/response
- Error handling (401, 403, etc.)
- Token expiration (30 days)
- Password validation

Generate complete auth.py route file with all endpoints.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=3000
        )
        
        return self._extract_code(code)
    
    async def _generate_routes(self, pm_spec: Dict, db_schema: Dict) -> Dict[str, str]:
        """Generate CRUD route files for each entity"""
        
        routes = {}
        models = db_schema.get('models', {})
        
        for model_name in models.keys():
            logger.info(f"Generating routes for {model_name}...")
            
            prompt = f"""
Create FastAPI CRUD routes for {model_name} model.

Requirements:
1. GET /{model_name.lower()}s - List all (with pagination, filtering)
2. GET /{model_name.lower()}s/{{id}} - Get by ID
3. POST /{model_name.lower()}s - Create new
4. PUT /{model_name.lower()}s/{{id}} - Update
5. DELETE /{model_name.lower()}s/{{id}} - Delete

Include:
- Proper authentication (Depends on get_current_user)
- Request validation (Pydantic schemas)
- Error handling (404, 400, etc.)
- Pagination (limit, offset)
- Filtering and sorting
- Proper HTTP status codes

Generate complete {model_name.lower()}s.py route file.
"""
            
            code = await self.qwen_client.generate_code(
                prompt=prompt,
                temperature=0.2,
                max_tokens=3000
            )
            
            routes[f"{model_name.lower()}s"] = self._extract_code(code)
        
        return routes
    
    async def _generate_schemas(self, db_schema: Dict) -> Dict[str, str]:
        """Generate Pydantic schemas for request/response validation"""
        
        schemas = {}
        models = db_schema.get('models', {})
        
        for model_name in models.keys():
            prompt = f"""
Create Pydantic schemas for {model_name} model.

Requirements:
1. {model_name}Base - Base schema with common fields
2. {model_name}Create - For POST requests (no ID)
3. {model_name}Update - For PUT requests (optional fields)
4. {model_name}Response - For responses (includes ID, timestamps)

Include:
- Field validation (email, min/max length, etc.)
- Optional vs required fields
- Proper type hints
- Examples in docstrings

Generate complete schemas for {model_name}.
"""
            
            code = await self.qwen_client.generate_code(
                prompt=prompt,
                temperature=0.2,
                max_tokens=2000
            )
            
            schemas[model_name.lower()] = self._extract_code(code)
        
        return schemas
    
    async def _generate_dependencies(self, pm_spec: Dict) -> str:
        """Generate FastAPI dependencies (database session, auth, etc.)"""
        
        prompt = """
Create FastAPI dependencies file.

Requirements:
1. get_db() - Database session dependency
2. get_current_user() - Extract user from JWT token
3. get_current_active_user() - Check if user is active
4. require_admin() - Admin-only dependency

Include:
- Proper error handling
- Session management
- Token validation

Generate complete dependencies.py file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=2000
        )
        
        return self._extract_code(code)
    
    async def _generate_config(self) -> str:
        """Generate configuration file"""
        
        prompt = """
Create a configuration file using Pydantic Settings.

Requirements:
1. Database URL
2. JWT secret key
3. JWT algorithm and expiration
4. CORS origins
5. Environment-based config (dev/prod)

Use Pydantic BaseSettings for environment variables.

Generate complete config.py file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=1500
        )
        
        return self._extract_code(code)
    
    def _extract_code(self, response: str) -> str:
        """Extract code from markdown blocks"""
        response = response.strip()
        
        # Remove markdown code blocks
        if "```python" in response:
            response = response.split("```python")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        return response
    
    def generate_summary(self, backend: Dict) -> str:
        """Generate human-readable summary"""
        
        routes_count = len(backend.get('routes', {}))
        schemas_count = len(backend.get('schemas', {}))
        
        summary = f"""
🚀 BACKEND API SUMMARY

**Framework:** FastAPI
**Authentication:** JWT (Bearer token)

**Files Generated:**
  • main.py - Application entry point
  • routes/auth.py - Authentication endpoints
  • routes/ - {routes_count} CRUD route files
  • schemas/ - {schemas_count} Pydantic schemas
  • dependencies.py - Auth & DB dependencies
  • config.py - Configuration management

**API Endpoints:**
  • POST /auth/register - User registration
  • POST /auth/login - User login (get JWT)
  • POST /auth/refresh - Refresh token
  • CRUD operations for all entities

**Features:**
  ✅ JWT authentication
  ✅ Password hashing (bcrypt)
  ✅ Request validation (Pydantic)
  ✅ Error handling
  ✅ CORS configuration
  ✅ Pagination & filtering
  ✅ Database session management
"""
        return summary


async def test_backend_developer():
    """Test the Backend Developer Agent"""
    from src.utils.qwen_client import get_qwen_client
    from src.agents.product_manager import ProductManagerAgent
    from src.agents.database_architect import DatabaseArchitectAgent
    
    client = get_qwen_client()
    
    # Step 1: Get PM spec
    print("Step 1: Getting PM specification...")
    pm_agent = ProductManagerAgent(client)
    pm_spec = await pm_agent.analyze_requirements(
        "Build a simple blog platform with user authentication"
    )
    
    # Step 2: Design database
    print("\nStep 2: Designing database schema...")
    db_architect = DatabaseArchitectAgent(client)
    db_schema = await db_architect.design_schema(pm_spec)
    
    # Step 3: Generate backend
    print("\nStep 3: Generating FastAPI backend...")
    backend_dev = BackendDeveloperAgent(client)
    backend = await backend_dev.generate_backend(pm_spec, db_schema)
    
    print("\n" + "="*60)
    print(backend_dev.generate_summary(backend))
    print("="*60)
    
    print("\n📝 Generated Files:")
    print("  ✅ main.py")
    print("  ✅ routes/auth.py")
    for route_name in backend.get('routes', {}).keys():
        print(f"  ✅ routes/{route_name}.py")
    for schema_name in backend.get('schemas', {}).keys():
        print(f"  ✅ schemas/{schema_name}.py")
    print("  ✅ dependencies.py")
    print("  ✅ config.py")
    
    print("\n💾 Sample: main.py (first 500 chars)")
    print("-" * 60)
    print(backend['main_app'][:500] + "...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_backend_developer())