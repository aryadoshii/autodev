"""Technical Writer Agent"""
import sys
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TechnicalWriterAgent:
    """
    Agent responsible for:
    - Generating comprehensive README.md
    - Creating API documentation
    - Writing setup and installation guides
    - Documenting architecture
    - Creating troubleshooting guides
    """
    
    def __init__(self, qwen_client):
        self.qwen_client = qwen_client
    
    async def generate_documentation(self, pm_spec: Dict, tech_stack: Dict) -> Dict:
        """
        Generate complete documentation
        
        Args:
            pm_spec: Product Manager specification
            tech_stack: Technology stack details
        
        Returns:
            Dict with all documentation files
        """
        logger.info("Starting documentation generation...")
        
        docs = {
            "readme": await self._generate_readme(pm_spec, tech_stack),
            "api_docs": await self._generate_api_docs(pm_spec),
            "architecture": await self._generate_architecture_docs(pm_spec, tech_stack),
            "setup_guide": await self._generate_setup_guide(pm_spec, tech_stack),
            "contributing": await self._generate_contributing_guide(),
            "troubleshooting": await self._generate_troubleshooting()
        }
        
        logger.success("Documentation generated")
        return docs
    
    async def _generate_readme(self, pm_spec: Dict, tech_stack: Dict) -> str:
        """Generate comprehensive README.md"""
        
        app_name = pm_spec.get('app_name', 'Application')
        description = pm_spec.get('description', 'A web application')
        features = pm_spec.get('core_features', [])
        
        features_str = '\n'.join([f"- {feature}" for feature in features])
        
        prompt = f"""
Create a comprehensive README.md for: {app_name}

Description: {description}

Core Features:
{features_str}

Tech Stack:
- Backend: {tech_stack.get('backend', 'FastAPI')}
- Frontend: {tech_stack.get('frontend', 'React')}
- Database: {tech_stack.get('database', 'PostgreSQL')}

README should include:
1. Project title and description
2. Features list
3. Tech stack with badges
4. Prerequisites
5. Installation instructions (both local and Docker)
6. Environment variables setup
7. Running the application
8. Running tests
9. API documentation link
10. Project structure overview
11. Contributing guide link
12. License
13. Screenshots section (placeholder)

Requirements:
- Use proper Markdown formatting
- Add badges (build status, coverage, license)
- Clear step-by-step instructions
- Professional and comprehensive
- Include quick start section

Generate complete README.md content.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=4000
        )
        
        return code.strip()
    
    async def _generate_api_docs(self, pm_spec: Dict) -> str:
        """Generate API documentation"""
        
        app_name = pm_spec.get('app_name', 'API')
        entities = pm_spec.get('data_entities', [])
        
        entities_str = '\n'.join([f"- {entity['name']}" for entity in entities])
        
        prompt = f"""
Create API documentation for {app_name}.

Entities: 
{entities_str}

Documentation should include:

1. Base URL and versioning
2. Authentication (JWT)
   - How to register
   - How to login
   - How to use tokens
   
3. Endpoints for each entity:
   - List all (GET /api/v1/items)
   - Get by ID (GET /api/v1/items/{{id}})
   - Create (POST /api/v1/items)
   - Update (PUT /api/v1/items/{{id}})
   - Delete (DELETE /api/v1/items/{{id}})
   
4. For each endpoint include:
   - HTTP method and path
   - Description
   - Request parameters
   - Request body (JSON example)
   - Response (JSON example)
   - Status codes
   - Error responses
   
5. Pagination, filtering, sorting

Requirements:
- Clear examples with curl commands
- Request/response JSON examples
- Error handling examples
- Authentication examples

Generate complete API.md content.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=4000
        )
        
        return code.strip()
    
    async def _generate_architecture_docs(self, pm_spec: Dict, tech_stack: Dict) -> str:
        """Generate architecture documentation"""
        
        app_name = pm_spec.get('app_name', 'Application')
        
        prompt = f"""
Create architecture documentation for {app_name}.

Tech Stack:
- Backend: {tech_stack.get('backend', 'FastAPI')}
- Frontend: {tech_stack.get('frontend', 'React')}
- Database: {tech_stack.get('database', 'PostgreSQL')}

Documentation should include:

1. System Overview
   - High-level architecture diagram (Mermaid)
   - Component interaction
   
2. Backend Architecture
   - Directory structure
   - Layer separation (routes, services, models)
   - Authentication flow
   - Database design
   
3. Frontend Architecture
   - Directory structure
   - Component hierarchy
   - State management
   - Routing
   
4. Data Flow
   - Request/response cycle
   - Authentication flow
   - CRUD operations flow
   
5. Database Schema
   - Entity-relationship diagram (Mermaid)
   - Table descriptions
   
6. Security
   - Authentication mechanism
   - Authorization
   - Data validation
   
7. Deployment Architecture
   - Docker containers
   - Services communication
   - Environment configuration

Use Mermaid diagrams where appropriate.

Generate complete ARCHITECTURE.md content.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=4000
        )
        
        return code.strip()
    
    async def _generate_setup_guide(self, pm_spec: Dict, tech_stack: Dict) -> str:
        """Generate detailed setup guide"""
        
        app_name = pm_spec.get('app_name', 'Application')
        
        prompt = f"""
Create a detailed setup guide for {app_name}.

Setup scenarios:
1. Local development (without Docker)
2. Docker development
3. Production deployment

For each scenario include:

**Local Development:**
1. Prerequisites installation
   - Python 3.11+
   - Node.js 20+
   - PostgreSQL 15+
   
2. Backend setup
   - Clone repository
   - Create virtual environment
   - Install dependencies
   - Setup database
   - Run migrations
   - Configure environment variables
   - Start server
   
3. Frontend setup
   - Install dependencies
   - Configure environment
   - Start dev server
   
4. Verification steps

**Docker Development:**
1. Prerequisites (Docker, Docker Compose)
2. Build and run with docker-compose
3. Access services
4. View logs
5. Stop services

**Production Deployment:**
1. Server requirements
2. Environment setup
3. Build process
4. Database setup
5. Deployment steps
6. Monitoring

Include troubleshooting tips for common issues.

Generate complete SETUP.md content.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=4000
        )
        
        return code.strip()
    
    async def _generate_contributing_guide(self) -> str:
        """Generate contributing guide"""
        
        prompt = """
Create a CONTRIBUTING.md guide for open-source contributors.

Include:

1. How to contribute
   - Report bugs
   - Suggest features
   - Submit pull requests
   
2. Development setup
   - Fork and clone
   - Create branch
   - Install dependencies
   
3. Coding standards
   - Code style (Black, ESLint)
   - Naming conventions
   - Documentation requirements
   
4. Testing requirements
   - Write tests for new features
   - Run test suite
   - Coverage requirements (80%+)
   
5. Commit guidelines
   - Conventional commits format
   - Clear commit messages
   
6. Pull request process
   - Create PR
   - Description requirements
   - Code review process
   - Merging
   
7. Code of conduct
   - Be respectful
   - Inclusive language
   
8. Getting help
   - Where to ask questions
   - Community channels

Generate complete CONTRIBUTING.md content.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=3000
        )
        
        return code.strip()
    
    async def _generate_troubleshooting(self) -> str:
        """Generate troubleshooting guide"""
        
        prompt = """
Create a TROUBLESHOOTING.md guide.

Common issues and solutions:

**Backend Issues:**
1. Database connection errors
   - Check DATABASE_URL
   - Verify PostgreSQL is running
   - Check credentials
   
2. Migration errors
   - Clear migration history
   - Drop and recreate database
   
3. Import errors
   - Verify virtual environment
   - Reinstall dependencies
   
4. JWT token errors
   - Check SECRET_KEY
   - Verify token expiration
   
**Frontend Issues:**
1. API connection errors
   - Check VITE_API_URL
   - Verify backend is running
   - Check CORS settings
   
2. Build errors
   - Clear node_modules
   - Reinstall dependencies
   - Check Node version
   
3. Routing issues
   - Verify React Router setup
   - Check route paths
   
**Docker Issues:**
1. Container won't start
   - Check logs
   - Verify environment variables
   - Check port conflicts
   
2. Volume permission errors
   - Fix file permissions
   - Use named volumes
   
3. Network issues
   - Check service names
   - Verify network configuration

**General Issues:**
1. Port already in use
2. Permission denied errors
3. Environment variables not loaded
4. Tests failing

For each issue provide:
- Symptoms
- Possible causes
- Step-by-step solutions
- Prevention tips

Generate complete TROUBLESHOOTING.md content.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=3500
        )
        
        return code.strip()
    
    def generate_summary(self, docs: Dict) -> str:
        """Generate human-readable summary"""
        
        summary = """
📚 DOCUMENTATION SUMMARY

**Generated Files:**
  ✅ README.md - Main project documentation
  ✅ API.md - Complete API reference
  ✅ ARCHITECTURE.md - System design and architecture
  ✅ SETUP.md - Detailed setup instructions
  ✅ CONTRIBUTING.md - Contribution guidelines
  ✅ TROUBLESHOOTING.md - Common issues and solutions

**README.md includes:**
  • Project overview and description
  • Features list
  • Tech stack with badges
  • Quick start guide
  • Installation instructions
  • Environment setup
  • Running tests
  • Project structure

**API.md includes:**
  • Authentication endpoints
  • CRUD endpoints for all entities
  • Request/response examples
  • Error handling
  • curl command examples

**ARCHITECTURE.md includes:**
  • System overview diagram
  • Component architecture
  • Data flow diagrams
  • Database schema (ERD)
  • Security design
  • Deployment architecture

**SETUP.md includes:**
  • Local development setup
  • Docker setup
  • Production deployment
  • Step-by-step instructions

**Quality:**
  ✅ Professional formatting
  ✅ Clear instructions
  ✅ Code examples
  ✅ Diagrams (Mermaid)
  ✅ Troubleshooting tips
  ✅ Best practices
"""
        return summary


async def test_technical_writer():
    """Test the Technical Writer Agent"""
    from src.utils.qwen_client import get_qwen_client
    from src.agents.product_manager import ProductManagerAgent
    
    client = get_qwen_client()
    
    # Get PM spec
    print("Step 1: Getting PM specification...")
    pm_agent = ProductManagerAgent(client)
    pm_spec = await pm_agent.analyze_requirements(
        "Build a task management app with teams"
    )
    
    # Generate documentation
    print("\nStep 2: Generating documentation...")
    writer = TechnicalWriterAgent(client)
    
    tech_stack = pm_spec.get('tech_stack', {
        'backend': 'FastAPI',
        'frontend': 'React',
        'database': 'PostgreSQL'
    })
    
    docs = await writer.generate_documentation(pm_spec, tech_stack)
    
    print("\n" + "="*60)
    print(writer.generate_summary(docs))
    print("="*60)
    
    print("\n📝 Documentation Files:")
    for doc_name in docs.keys():
        print(f"  ✅ {doc_name.upper()}.md")
    
    print("\n💾 Sample: README.md (first 500 chars)")
    print("-" * 60)
    print(docs['readme'][:500] + "...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_technical_writer())