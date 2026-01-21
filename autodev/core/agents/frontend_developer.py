"""Frontend Developer Agent"""
import sys
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class FrontendDeveloperAgent:
    """
    Agent responsible for:
    - Creating React application (Vite)
    - Building UI components
    - Implementing routing (React Router)
    - State management (Context API)
    - API integration (Axios)
    - Styling (Tailwind CSS)
    """
    
    def __init__(self, qwen_client):
        self.qwen_client = qwen_client
    
    async def generate_frontend(self, pm_spec: Dict, backend_spec: Dict) -> Dict:
        """
        Generate complete React frontend
        
        Args:
            pm_spec: Product Manager specification
            backend_spec: Backend API specification
        
        Returns:
            Dict with all frontend files
        """
        logger.info("Starting frontend generation...")
        
        frontend = {
            "app": await self._generate_app_component(pm_spec),
            "main": await self._generate_main_entry(pm_spec),
            "components": await self._generate_components(pm_spec),
            "pages": await self._generate_pages(pm_spec),
            "contexts": await self._generate_contexts(),
            "services": await self._generate_api_service(backend_spec),
            "config": {
                "package_json": await self._generate_package_json(pm_spec),
                "tailwind_config": await self._generate_tailwind_config(),
                "vite_config": await self._generate_vite_config()
            }
        }
        
        logger.success(f"Frontend generated with {len(frontend['components'])} components")
        return frontend
    
    async def _generate_app_component(self, pm_spec: Dict) -> str:
        """Generate main App.jsx component with routing"""
        
        app_name = pm_spec.get('app_name', 'App')
        
        prompt = f"""
Create the main App.jsx component for {app_name}.

Requirements:
1. Setup React Router with routes:
   - / (Home/Dashboard)
   - /login (Login page)
   - /register (Register page)
   - Protected routes that require authentication
2. Use AuthContext for authentication state
3. Add a Layout component with Header/Footer
4. Handle loading states
5. Implement protected route wrapper

Include:
- React Router v6
- Context API integration
- Clean component structure
- Proper routing setup

Generate complete App.jsx file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=2500
        )
        
        return self._extract_code(code)
    
    async def _generate_main_entry(self, pm_spec: Dict) -> str:
        """Generate main.jsx entry point"""
        
        prompt = """
Create the main.jsx entry point for React application.

Requirements:
1. Import React and ReactDOM
2. Import App component
3. Import global CSS (index.css with Tailwind)
4. Setup StrictMode
5. Render to root element

Generate complete main.jsx file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=1000
        )
        
        return self._extract_code(code)
    
    async def _generate_components(self, pm_spec: Dict) -> Dict[str, str]:
        """Generate reusable UI components"""
        
        components = {}
        
        component_list = [
            ("Button", "Reusable button component with variants (primary, secondary, danger)"),
            ("Input", "Form input component with label, error message, and validation"),
            ("Card", "Card container component for content display"),
            ("Modal", "Modal dialog component with overlay"),
            ("Layout", "Layout component with Header, Sidebar (optional), and Footer"),
            ("Navbar", "Navigation bar with logo, links, and user menu"),
            ("LoadingSpinner", "Loading spinner component")
        ]
        
        for component_name, description in component_list:
            logger.info(f"Generating {component_name} component...")
            
            prompt = f"""
Create a React {component_name} component.

Description: {description}

Requirements:
1. Use functional component with hooks
2. Style with Tailwind CSS
3. Add PropTypes for type checking
4. Make it reusable and configurable
5. Include proper accessibility (ARIA)

Generate complete {component_name}.jsx file.
"""
            
            code = await self.qwen_client.generate_code(
                prompt=prompt,
                temperature=0.2,
                max_tokens=2000
            )
            
            components[component_name] = self._extract_code(code)
        
        return components
    
    async def _generate_pages(self, pm_spec: Dict) -> Dict[str, str]:
        """Generate page components"""
        
        pages = {}
        
        page_list = [
            ("Login", "Login page with email/password form and JWT authentication"),
            ("Register", "Registration page with form validation"),
            ("Dashboard", "Main dashboard page showing overview"),
            ("NotFound", "404 page for invalid routes")
        ]
        
        # Add entity-specific pages based on PM spec
        entities = pm_spec.get('data_entities', [])
        for entity in entities[:2]:  # Limit to first 2 to save time
            entity_name = entity.get('name', 'Item')
            page_list.append(
                (f"{entity_name}List", f"List page for {entity_name} with CRUD operations")
            )
        
        for page_name, description in page_list:
            logger.info(f"Generating {page_name} page...")
            
            prompt = f"""
Create a React {page_name} page component.

Description: {description}

Requirements:
1. Use functional component with hooks (useState, useEffect)
2. Integrate with API service
3. Use AuthContext for authentication
4. Style with Tailwind CSS
5. Add loading and error states
6. Include form validation (if applicable)
7. Show success/error messages

Generate complete {page_name}.jsx file.
"""
            
            code = await self.qwen_client.generate_code(
                prompt=prompt,
                temperature=0.2,
                max_tokens=3000
            )
            
            pages[page_name] = self._extract_code(code)
        
        return pages
    
    async def _generate_contexts(self) -> Dict[str, str]:
        """Generate React Context for state management"""
        
        contexts = {}
        
        # Auth Context
        prompt = """
Create an AuthContext for managing authentication state.

Requirements:
1. Store user data and token in state
2. Provide login function (call API, store token)
3. Provide logout function (clear token)
4. Provide register function
5. Auto-load user from localStorage on mount
6. Store token in localStorage
7. Provide isAuthenticated, user, loading states

Include:
- Context creation
- Provider component
- Custom useAuth hook

Generate complete AuthContext.jsx file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=3000
        )
        
        contexts['AuthContext'] = self._extract_code(code)
        
        return contexts
    
    async def _generate_api_service(self, backend_spec: Dict) -> str:
        """Generate API client service"""
        
        prompt = """
Create an API service module using Axios.

Requirements:
1. Create axios instance with base URL
2. Add request interceptor (attach JWT token)
3. Add response interceptor (handle 401 errors)
4. Export API methods:
   - auth.login(email, password)
   - auth.register(userData)
   - auth.logout()
   - users.getAll()
   - users.getById(id)
   - users.create(data)
   - users.update(id, data)
   - users.delete(id)

Include:
- Token management
- Error handling
- Request/response interceptors

Generate complete api.js file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=3000
        )
        
        return self._extract_code(code)
    
    async def _generate_package_json(self, pm_spec: Dict) -> str:
        """Generate package.json"""
        
        app_name = pm_spec.get('app_name', 'frontend-app')
        
        package_json = {
            "name": app_name,
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview",
                "lint": "eslint . --ext js,jsx"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.20.0",
                "axios": "^1.6.2"
            },
            "devDependencies": {
                "@types/react": "^18.2.43",
                "@types/react-dom": "^18.2.17",
                "@vitejs/plugin-react": "^4.2.1",
                "autoprefixer": "^10.4.16",
                "eslint": "^8.55.0",
                "postcss": "^8.4.32",
                "tailwindcss": "^3.3.6",
                "vite": "^5.0.8"
            }
        }
        
        return json.dumps(package_json, indent=2)
    
    async def _generate_tailwind_config(self) -> str:
        """Generate Tailwind CSS config"""
        
        config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
      },
    },
  },
  plugins: [],
}"""
        return config
    
    async def _generate_vite_config(self) -> str:
        """Generate Vite config"""
        
        config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})"""
        return config
    
    def _extract_code(self, response: str) -> str:
        """Extract code from markdown blocks"""
        response = response.strip()
        
        # Remove markdown code blocks
        if "```jsx" in response:
            response = response.split("```jsx")[1].split("```")[0].strip()
        elif "```javascript" in response:
            response = response.split("```javascript")[1].split("```")[0].strip()
        elif "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        return response
    
    def generate_summary(self, frontend: Dict) -> str:
        """Generate human-readable summary"""
        
        components_count = len(frontend.get('components', {}))
        pages_count = len(frontend.get('pages', {}))
        
        summary = f"""
⚛️  REACT FRONTEND SUMMARY

**Framework:** React 18 + Vite
**Styling:** Tailwind CSS
**Routing:** React Router v6
**State:** Context API
**HTTP Client:** Axios

**Files Generated:**
  • src/App.jsx - Main app with routing
  • src/main.jsx - Entry point
  • src/components/ - {components_count} reusable components
  • src/pages/ - {pages_count} page components
  • src/contexts/AuthContext.jsx - Authentication state
  • src/services/api.js - API client
  • package.json - Dependencies
  • tailwind.config.js - Tailwind setup
  • vite.config.js - Vite configuration

**Components:**
  ✅ Button, Input, Card, Modal
  ✅ Layout, Navbar, LoadingSpinner

**Pages:**
  ✅ Login, Register, Dashboard
  ✅ Entity list/detail pages
  ✅ 404 Not Found

**Features:**
  ✅ JWT authentication
  ✅ Protected routes
  ✅ Form validation
  ✅ Error handling
  ✅ Loading states
  ✅ Responsive design (Tailwind)
  ✅ API integration
"""
        return summary


async def test_frontend_developer():
    """Test the Frontend Developer Agent"""
    from src.utils.qwen_client import get_qwen_client
    from src.agents.product_manager import ProductManagerAgent
    from src.agents.backend_developer import BackendDeveloperAgent
    from src.agents.database_architect import DatabaseArchitectAgent
    
    client = get_qwen_client()
    
    # Step 1: Get PM spec
    print("Step 1: Getting PM specification...")
    pm_agent = ProductManagerAgent(client)
    pm_spec = await pm_agent.analyze_requirements(
        "Build a simple blog with posts and comments"
    )
    
    # Step 2: Design database (needed for context)
    print("\nStep 2: Designing database schema...")
    db_architect = DatabaseArchitectAgent(client)
    db_schema = await db_architect.design_schema(pm_spec)
    
    # Step 3: Generate backend (needed for API spec)
    print("\nStep 3: Generating backend API...")
    backend_dev = BackendDeveloperAgent(client)
    backend = await backend_dev.generate_backend(pm_spec, db_schema)
    
    # Step 4: Generate frontend
    print("\nStep 4: Generating React frontend...")
    frontend_dev = FrontendDeveloperAgent(client)
    frontend = await frontend_dev.generate_frontend(pm_spec, backend)
    
    print("\n" + "="*60)
    print(frontend_dev.generate_summary(frontend))
    print("="*60)
    
    print("\n📝 Generated Components:")
    for comp_name in frontend.get('components', {}).keys():
        print(f"  ✅ {comp_name}.jsx")
    
    print("\n📄 Generated Pages:")
    for page_name in frontend.get('pages', {}).keys():
        print(f"  ✅ {page_name}.jsx")
    
    print("\n💾 Sample: App.jsx (first 400 chars)")
    print("-" * 60)
    print(frontend['app'][:400] + "...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_frontend_developer())