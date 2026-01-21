"""QA Engineer Agent"""
import sys
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class QAEngineerAgent:
    """
    Agent responsible for:
    - Generating unit tests (pytest, Jest)
    - Creating API integration tests
    - Writing E2E tests (Playwright)
    - Setting up test fixtures and mocks
    - Generating test coverage reports
    """
    
    def __init__(self, qwen_client):
        self.qwen_client = qwen_client
    
    async def generate_tests(self, pm_spec: Dict, backend_spec: Dict, frontend_spec: Dict) -> Dict:
        """
        Generate comprehensive test suite
        
        Args:
            pm_spec: Product Manager specification
            backend_spec: Backend code specification
            frontend_spec: Frontend code specification
        
        Returns:
            Dict with all test files
        """
        logger.info("Starting test generation...")
        
        tests = {
            "backend": await self._generate_backend_tests(pm_spec, backend_spec),
            "frontend": await self._generate_frontend_tests(pm_spec, frontend_spec),
            "e2e": await self._generate_e2e_tests(pm_spec),
            "config": {
                "pytest_ini": await self._generate_pytest_config(),
                "jest_config": await self._generate_jest_config(),
                "playwright_config": await self._generate_playwright_config()
            }
        }
        
        total_tests = (
            len(tests['backend']) + 
            len(tests['frontend']) + 
            len(tests['e2e'])
        )
        
        logger.success(f"Test suite generated with {total_tests} test files")
        return tests
    
    async def _generate_backend_tests(self, pm_spec: Dict, backend_spec: Dict) -> Dict[str, str]:
        """Generate pytest tests for backend"""
        
        backend_tests = {}
        
        # Test authentication
        logger.info("Generating auth tests...")
        prompt = """
Create comprehensive pytest tests for authentication endpoints.

Test cases:
1. User registration (success, duplicate email, invalid data)
2. User login (success, wrong password, non-existent user)
3. Token refresh (valid token, expired token, invalid token)
4. Protected endpoint access (with token, without token, invalid token)

Requirements:
- Use pytest fixtures for test data
- Use pytest-asyncio for async tests
- Mock database with conftest.py fixtures
- Test both happy paths and error cases
- Use httpx.AsyncClient for API testing
- Assert proper status codes and response data

Generate complete test_auth.py file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=3500
        )
        backend_tests['test_auth'] = self._extract_code(code)
        
        # Test CRUD operations
        entities = pm_spec.get('data_entities', [])
        for entity in entities[:2]:  # Limit to 2 entities
            entity_name = entity.get('name', 'Item')
            logger.info(f"Generating tests for {entity_name}...")
            
            prompt = f"""
Create pytest tests for {entity_name} CRUD operations.

Test cases:
1. Create {entity_name} (success, invalid data, unauthorized)
2. Get all {entity_name}s (with pagination, filtering)
3. Get {entity_name} by ID (success, not found)
4. Update {entity_name} (success, not found, unauthorized)
5. Delete {entity_name} (success, not found, unauthorized)

Requirements:
- Use fixtures for test data
- Test authentication/authorization
- Validate response schemas
- Test edge cases

Generate complete test_{entity_name.lower()}s.py file.
"""
            
            code = await self.qwen_client.generate_code(
                prompt=prompt,
                temperature=0.2,
                max_tokens=3500
            )
            backend_tests[f'test_{entity_name.lower()}s'] = self._extract_code(code)
        
        # Conftest for fixtures
        logger.info("Generating backend conftest...")
        prompt = """
Create pytest conftest.py with fixtures for backend testing.

Fixtures needed:
1. test_db - Test database session
2. client - AsyncClient for API testing
3. test_user - Create test user
4. auth_headers - Headers with valid JWT token
5. mock_data - Sample data for entities

Requirements:
- Setup/teardown test database
- Create tables before tests
- Clean up after tests
- Provide reusable fixtures

Generate complete conftest.py file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=3000
        )
        backend_tests['conftest'] = self._extract_code(code)
        
        return backend_tests
    
    async def _generate_frontend_tests(self, pm_spec: Dict, frontend_spec: Dict) -> Dict[str, str]:
        """Generate Jest/React Testing Library tests"""
        
        frontend_tests = {}
        
        # Test components
        components = ['Button', 'Input', 'Modal', 'Navbar']
        
        for component in components:
            logger.info(f"Generating tests for {component} component...")
            
            prompt = f"""
Create Jest + React Testing Library tests for {component} component.

Test cases:
1. Component renders correctly
2. Props are handled properly
3. User interactions work (clicks, input changes)
4. Conditional rendering works
5. Accessibility attributes present

Requirements:
- Use @testing-library/react
- Test user interactions with fireEvent/userEvent
- Check accessibility (aria labels)
- Test edge cases
- Use proper assertions

Generate complete {component}.test.jsx file.
"""
            
            code = await self.qwen_client.generate_code(
                prompt=prompt,
                temperature=0.2,
                max_tokens=2500
            )
            frontend_tests[f'{component}.test'] = self._extract_code(code)
        
        # Test pages
        logger.info("Generating Login page tests...")
        prompt = """
Create tests for Login page component.

Test cases:
1. Form renders with email and password fields
2. Form validation (empty fields, invalid email)
3. Successful login (mock API call)
4. Failed login (wrong credentials)
5. Redirect after successful login
6. Loading state during login
7. Error messages display

Requirements:
- Mock API calls with jest.mock
- Test form submission
- Test navigation
- Test error handling

Generate complete Login.test.jsx file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=3000
        )
        frontend_tests['Login.test'] = self._extract_code(code)
        
        # Test API service
        logger.info("Generating API service tests...")
        prompt = """
Create tests for API service module.

Test cases:
1. API client initialized correctly
2. Request interceptor adds token
3. Response interceptor handles 401
4. Auth methods work (login, register, logout)
5. CRUD methods work
6. Error handling works

Requirements:
- Mock axios
- Test interceptors
- Test error handling
- Verify correct endpoints called

Generate complete api.test.js file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=2500
        )
        frontend_tests['api.test'] = self._extract_code(code)
        
        return frontend_tests
    
    async def _generate_e2e_tests(self, pm_spec: Dict) -> Dict[str, str]:
        """Generate Playwright E2E tests"""
        
        e2e_tests = {}
        
        logger.info("Generating E2E user flow tests...")
        prompt = """
Create Playwright E2E tests for complete user flow.

Test scenarios:
1. User Registration Flow
   - Navigate to register page
   - Fill form with valid data
   - Submit and verify success
   - Verify redirect to login/dashboard

2. User Login Flow
   - Navigate to login page
   - Enter credentials
   - Submit and verify token stored
   - Verify redirect to dashboard

3. CRUD Operations Flow
   - Login as user
   - Create new item
   - View item in list
   - Edit item
   - Delete item
   - Verify item deleted

4. Authentication Flow
   - Access protected page without login
   - Verify redirect to login
   - Login and access protected page
   - Logout and verify redirect

Requirements:
- Use Playwright best practices
- Add page object models
- Use proper selectors
- Add assertions at each step
- Handle async operations
- Add screenshots on failure

Generate complete user-flow.spec.js file.
"""
        
        code = await self.qwen_client.generate_code(
            prompt=prompt,
            temperature=0.2,
            max_tokens=4000
        )
        e2e_tests['user-flow.spec'] = self._extract_code(code)
        
        return e2e_tests
    
    async def _generate_pytest_config(self) -> str:
        """Generate pytest.ini configuration"""
        
        config = """[pytest]
testpaths = tests/backend
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
addopts = 
    --verbose
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
"""
        return config
    
    async def _generate_jest_config(self) -> str:
        """Generate Jest configuration"""
        
        config = """export default {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  moduleNameMapper: {
    '\\\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  transform: {
    '^.+\\\\.(js|jsx)$': 'babel-jest',
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx}',
    '!src/main.jsx',
    '!src/**/*.test.{js,jsx}',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};"""
        return config
    
    async def _generate_playwright_config(self) -> str:
        """Generate Playwright configuration"""
        
        config = """import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});"""
        return config
    
    def _extract_code(self, response: str) -> str:
        """Extract code from markdown blocks"""
        response = response.strip()
        
        if "```python" in response:
            response = response.split("```python")[1].split("```")[0].strip()
        elif "```javascript" in response:
            response = response.split("```javascript")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        return response
    
    def generate_summary(self, tests: Dict) -> str:
        """Generate human-readable summary"""
        
        backend_count = len(tests.get('backend', {}))
        frontend_count = len(tests.get('frontend', {}))
        e2e_count = len(tests.get('e2e', {}))
        
        summary = f"""
🧪 TEST SUITE SUMMARY

**Backend Tests (pytest):** {backend_count} files
  • test_auth.py - Authentication tests
  • test_*.py - CRUD operation tests
  • conftest.py - Test fixtures

**Frontend Tests (Jest):** {frontend_count} files
  • Component tests (Button, Input, Modal, Navbar)
  • Page tests (Login, Register, Dashboard)
  • API service tests

**E2E Tests (Playwright):** {e2e_count} files
  • Complete user flows
  • Authentication scenarios
  • CRUD workflows

**Coverage Goals:**
  ✅ Backend: 80%+ code coverage
  ✅ Frontend: 80%+ code coverage
  ✅ E2E: Critical user paths

**Test Types:**
  ✅ Unit tests (individual functions/components)
  ✅ Integration tests (API endpoints)
  ✅ E2E tests (full user workflows)

**Configuration:**
  • pytest.ini - Backend test config
  • jest.config.js - Frontend test config
  • playwright.config.js - E2E test config
"""
        return summary


async def test_qa_engineer():
    """Test the QA Engineer Agent"""
    from src.utils.qwen_client import get_qwen_client
    from src.agents.product_manager import ProductManagerAgent
    
    client = get_qwen_client()
    
    # Get PM spec
    print("Step 1: Getting PM specification...")
    pm_agent = ProductManagerAgent(client)
    pm_spec = await pm_agent.analyze_requirements(
        "Build a task management app"
    )
    
    # Generate tests (mock backend/frontend specs for demo)
    print("\nStep 2: Generating test suite...")
    qa_engineer = QAEngineerAgent(client)
    tests = await qa_engineer.generate_tests(pm_spec, {}, {})
    
    print("\n" + "="*60)
    print(qa_engineer.generate_summary(tests))
    print("="*60)
    
    print("\n📝 Backend Tests Generated:")
    for test_name in tests.get('backend', {}).keys():
        print(f"  ✅ {test_name}.py")
    
    print("\n📄 Frontend Tests Generated:")
    for test_name in tests.get('frontend', {}).keys():
        print(f"  ✅ {test_name}")
    
    print("\n🎭 E2E Tests Generated:")
    for test_name in tests.get('e2e', {}).keys():
        print(f"  ✅ {test_name}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_qa_engineer())