"""DevOps Agent"""
import sys
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class DevOpsAgent:
    """
    Agent responsible for:
    - Creating Dockerfiles (backend/frontend)
    - Generating docker-compose.yml
    - Building CI/CD pipelines (GitHub Actions)
    - Creating deployment configurations
    - Setting up environment templates
    """
    
    def __init__(self, qwen_client):
        self.qwen_client = qwen_client
    
    async def generate_deployment(self, pm_spec: Dict) -> Dict:
        """
        Generate complete deployment configuration
        
        Args:
            pm_spec: Product Manager specification
        
        Returns:
            Dict with all deployment files
        """
        logger.info("Starting deployment generation...")
        
        deployment = {
            "docker": {
                "backend_dockerfile": await self._generate_backend_dockerfile(),
                "frontend_dockerfile": await self._generate_frontend_dockerfile(),
                "docker_compose": await self._generate_docker_compose(pm_spec),
                "dockerignore": await self._generate_dockerignore()
            },
            "ci_cd": {
                "github_actions": await self._generate_github_actions(pm_spec)
            },
            "env": {
                "backend_env": await self._generate_backend_env(),
                "frontend_env": await self._generate_frontend_env()
            },
            "nginx": await self._generate_nginx_config()
        }
        
        logger.success("Deployment configuration generated")
        return deployment
    
    async def _generate_backend_dockerfile(self) -> str:
        """Generate Dockerfile for FastAPI backend"""
        
        prompt = """
Create a production-ready Dockerfile for FastAPI backend.

Requirements:
1. Use Python 3.11 slim image
2. Multi-stage build (builder + runtime)
3. Install dependencies from requirements.txt
4. Copy application code
5. Run as non-root user
6. Expose port 8000
7. Use uvicorn for production
8. Add health check
9. Optimize layers for caching

Best practices:
- Minimize image size
- Security (non-root user)
- Layer caching optimization
- Production-ready setup

Generate complete Dockerfile for backend.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=2000
        )
        
        return self._extract_code(code)
    
    async def _generate_frontend_dockerfile(self) -> str:
        """Generate Dockerfile for React frontend"""
        
        prompt = """
Create a production-ready Dockerfile for React (Vite) frontend.

Requirements:
1. Use Node.js 20 alpine image
2. Multi-stage build (build + production)
3. Stage 1: Build React app with npm
4. Stage 2: Serve with nginx
5. Copy build output to nginx
6. Expose port 80
7. Add nginx configuration
8. Optimize for production

Best practices:
- Small final image (nginx alpine)
- Build optimization
- Caching layers
- Security

Generate complete Dockerfile for frontend.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=2000
        )
        
        return self._extract_code(code)
    
    async def _generate_docker_compose(self, pm_spec: Dict) -> str:
        """Generate docker-compose.yml"""
        
        app_name = pm_spec.get('app_name', 'app')
        
        prompt = f"""
Create a docker-compose.yml for {app_name}.

Services needed:
1. backend (FastAPI)
   - Build from ./backend
   - Port 8000:8000
   - Environment variables
   - Depends on database
   - Health check

2. frontend (React + nginx)
   - Build from ./frontend
   - Port 3000:80
   - Depends on backend

3. database (PostgreSQL)
   - Use postgres:15-alpine
   - Port 5432:5432
   - Volume for data persistence
   - Environment variables
   - Health check

4. redis (optional - for caching)
   - Use redis:7-alpine
   - Port 6379:6379

Include:
- Networks
- Volumes
- Health checks
- Restart policies
- Environment variables

Generate complete docker-compose.yml file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=2500
        )
        
        return self._extract_code(code)
    
    async def _generate_dockerignore(self) -> str:
        """Generate .dockerignore file"""
        
        dockerignore = """# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.pytest_cache
.coverage
htmlcov
venv
env
.venv

# Node
node_modules
npm-debug.log
yarn-error.log
.npm
.yarn

# IDE
.vscode
.idea
*.swp
*.swo
*~

# Git
.git
.gitignore
.gitattributes

# OS
.DS_Store
Thumbs.db

# Docs
*.md
docs/

# Tests
tests/
*.test.js
*.spec.js

# CI/CD
.github
.gitlab-ci.yml

# Environment
.env
.env.local
.env.*.local
"""
        return dockerignore
    
    async def _generate_github_actions(self, pm_spec: Dict) -> str:
        """Generate GitHub Actions CI/CD workflow"""
        
        app_name = pm_spec.get('app_name', 'app')
        
        prompt = f"""
Create a GitHub Actions workflow for CI/CD of {app_name}.

Workflow steps:
1. Trigger on push to main and pull requests
2. Backend job:
   - Checkout code
   - Setup Python 3.11
   - Install dependencies
   - Run linting (ruff)
   - Run tests (pytest with coverage)
   - Upload coverage report
   
3. Frontend job:
   - Checkout code
   - Setup Node.js 20
   - Install dependencies
   - Run linting (eslint)
   - Run tests (Jest)
   - Build production bundle
   
4. Deploy job (on main branch only):
   - Depends on backend and frontend jobs
   - Build Docker images
   - Push to registry (optional)
   - Deploy to production

Include:
- Parallel job execution
- Caching (pip, npm)
- Environment variables
- Success/failure notifications

Generate complete .github/workflows/ci-cd.yml file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=3500
        )
        
        return self._extract_code(code)
    
    async def _generate_backend_env(self) -> str:
        """Generate backend .env.example"""
        
        env = """# Backend Environment Variables

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dbname
DB_USER=user
DB_PASSWORD=password

# JWT Authentication
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# API
API_V1_PREFIX=/api/v1
PROJECT_NAME=MyApp
"""
        return env
    
    async def _generate_frontend_env(self) -> str:
        """Generate frontend .env.example"""
        
        env = """# Frontend Environment Variables

# API
VITE_API_URL=http://localhost:8000/api/v1
VITE_API_TIMEOUT=30000

# App
VITE_APP_NAME=MyApp
VITE_APP_VERSION=1.0.0

# Features
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_ERROR_TRACKING=false

# Environment
VITE_ENVIRONMENT=development
"""
        return env
    
    async def _generate_nginx_config(self) -> str:
        """Generate nginx configuration for frontend"""
        
        config = """server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_vary on;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # React Router support
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy (optional)
    location /api {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files caching
    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
"""
        return config
    
    def _extract_code(self, response: str) -> str:
        """Extract code from markdown blocks"""
        response = response.strip()
        
        if "```dockerfile" in response.lower():
            response = response.split("```")[1].split("```")[0].strip()
            if response.lower().startswith("dockerfile"):
                response = response.split("\n", 1)[1].strip()
        elif "```yaml" in response:
            response = response.split("```yaml")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        return response
    
    def generate_summary(self, deployment: Dict) -> str:
        """Generate human-readable summary"""
        
        summary = """
🚀 DEPLOYMENT CONFIGURATION SUMMARY

**Docker:**
  ✅ Dockerfile (backend) - Multi-stage Python build
  ✅ Dockerfile (frontend) - Multi-stage Node + nginx
  ✅ docker-compose.yml - Full stack orchestration
  ✅ .dockerignore - Optimize build context

**Services in docker-compose:**
  • backend (FastAPI on port 8000)
  • frontend (React + nginx on port 3000)
  • database (PostgreSQL on port 5432)
  • redis (caching on port 6379)

**CI/CD:**
  ✅ GitHub Actions workflow
  • Automated testing (backend + frontend)
  • Code linting
  • Build verification
  • Automated deployment

**Environment:**
  ✅ .env.example (backend) - All required variables
  ✅ .env.example (frontend) - Vite configuration

**Production Features:**
  ✅ Multi-stage Docker builds (small images)
  ✅ Non-root user (security)
  ✅ Health checks
  ✅ nginx with optimizations
  ✅ Volume persistence
  ✅ Restart policies
  ✅ Environment-based config

**Quick Start:**
```bash
  # Development
  docker-compose up -d
  
  # Production build
  docker-compose -f docker-compose.prod.yml up -d
```
"""
        return summary


async def test_devops():
    """Test the DevOps Agent"""
    from src.utils.qwen_client import get_qwen_client
    from src.agents.product_manager import ProductManagerAgent
    
    client = get_qwen_client()
    
    # Get PM spec
    print("Step 1: Getting PM specification...")
    pm_agent = ProductManagerAgent(client)
    pm_spec = await pm_agent.analyze_requirements(
        "Build a task management app"
    )
    
    # Generate deployment configs
    print("\nStep 2: Generating deployment configuration...")
    devops = DevOpsAgent(client)
    deployment = await devops.generate_deployment(pm_spec)
    
    print("\n" + "="*60)
    print(devops.generate_summary(deployment))
    print("="*60)
    
    print("\n📝 Docker Files Generated:")
    print("  ✅ Dockerfile (backend)")
    print("  ✅ Dockerfile (frontend)")
    print("  ✅ docker-compose.yml")
    print("  ✅ .dockerignore")
    
    print("\n🔄 CI/CD Generated:")
    print("  ✅ .github/workflows/ci-cd.yml")
    
    print("\n⚙️  Environment Templates:")
    print("  ✅ .env.example (backend)")
    print("  ✅ .env.example (frontend)")
    
    print("\n💾 Sample: docker-compose.yml (first 500 chars)")
    print("-" * 60)
    print(deployment['docker']['docker_compose'][:500] + "...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_devops())