"""
Development Crew - CrewAI Framework Implementation
Orchestrates 7 AI agents using proper CrewAI framework
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import os
from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from crewai import Agent, Task, Crew, Process
from autodev.api.client.qwen_llm import QwenLLM
from autodev.core.orchestrator.save_project import save_project_to_disk


class AutoDevCrew:
    """AutoDev Crew using CrewAI Framework"""
    
    def __init__(self):
        """Initialize the crew with Qwen LLM"""
        self.llm = QwenLLM()
        self.agents = self._create_agents()
        self.project_data = {}
        
    def _create_agents(self):
        """Create all 7 agents using CrewAI Agent class"""
        
        # Agent 1: Product Manager
        product_manager = Agent(
            role="Product Manager",
            goal="Analyze user requirements and create detailed product specifications",
            backstory="""You are an experienced Product Manager who excels at translating 
            user needs into detailed technical specifications. You identify core features, 
            data entities, and technical requirements.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Agent 2: Database Architect
        database_architect = Agent(
            role="Database Architect",
            goal="Design optimal database schemas with proper relationships and indexes",
            backstory="""You are a database expert who creates efficient, scalable database 
            designs using SQLAlchemy. You understand normalization, indexing, and relationships.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Agent 3: Backend Developer
        backend_developer = Agent(
            role="Backend Developer",
            goal="Build secure, scalable FastAPI backends with proper authentication",
            backstory="""You are a senior backend engineer specializing in FastAPI. 
            You write clean, well-documented code with JWT authentication, proper error 
            handling, and RESTful API design.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Agent 4: Frontend Developer
        frontend_developer = Agent(
            role="Frontend Developer",
            goal="Create beautiful, responsive React applications with Tailwind CSS",
            backstory="""You are a frontend expert who builds modern React applications. 
            You create reusable components, implement proper state management, and design 
            intuitive user interfaces.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Agent 5: QA Engineer
        qa_engineer = Agent(
            role="QA Engineer",
            goal="Write comprehensive test suites ensuring 80%+ code coverage",
            backstory="""You are a quality assurance expert who writes thorough tests. 
            You create unit tests, integration tests, and E2E tests using pytest, 
            Vitest, and Playwright.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Agent 6: DevOps Engineer
        devops_engineer = Agent(
            role="DevOps Engineer",
            goal="Setup production-ready deployment with Docker and CI/CD pipelines",
            backstory="""You are a DevOps specialist who containerizes applications 
            and sets up automated deployment pipelines. You create Docker configurations 
            and GitHub Actions workflows.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Agent 7: Technical Writer
        technical_writer = Agent(
            role="Technical Writer",
            goal="Create comprehensive, clear documentation for developers and users",
            backstory="""You are a documentation expert who writes clear, detailed 
            technical documentation. You create READMEs, API docs, setup guides, and 
            architecture documentation.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        return {
            'pm': product_manager,
            'db': database_architect,
            'backend': backend_developer,
            'frontend': frontend_developer,
            'qa': qa_engineer,
            'devops': devops_engineer,
            'writer': technical_writer
        }
    
    def _create_tasks(self, user_requirements: str):
        """Create tasks for each agent with proper dependencies"""
        
        # Task 1: Requirements Analysis
        pm_task = Task(
            description=f"""Analyze these requirements and create a detailed specification:
            
            Requirements: {user_requirements}
            
            Provide:
            1. Application name and type
            2. Core features (list)
            3. Data entities needed
            4. Tech stack (FastAPI, React, PostgreSQL, Tailwind)
            5. Authentication requirements
            
            Output as JSON with keys: app_name, app_type, core_features, data_entities, tech_stack, requires_auth
            """,
            agent=self.agents['pm'],
            expected_output="JSON specification with app details"
        )
        
        # Task 2: Database Design
        db_task = Task(
            description="""Based on the product specification, design the database schema.
            
            Create:
            1. SQLAlchemy models with proper types
            2. Relationships between models
            3. Indexes for performance
            4. Timestamps (created_at, updated_at)
            
            Output as JSON with keys: models (dict of model_name: code), relationships, indexes
            """,
            agent=self.agents['db'],
            expected_output="JSON with database schema and models",
            context=[pm_task]
        )
        
        # Task 3: Backend Development
        backend_task = Task(
            description="""Build the FastAPI backend with authentication.
            
            Create:
            1. main.py with FastAPI app
            2. JWT authentication (auth.py)
            3. CRUD routes for each entity
            4. Pydantic schemas
            5. Dependencies (database, auth)
            6. Config file
            
            Output as JSON with keys: main_app, auth, routes (dict), schemas (dict), dependencies, config
            """,
            agent=self.agents['backend'],
            expected_output="JSON with all backend code",
            context=[pm_task, db_task]
        )
        
        # Task 4: Frontend Development
        frontend_task = Task(
            description="""Create the React frontend with Tailwind CSS.
            
            Create:
            1. App.jsx with routing
            2. Reusable components (Button, Input, Card, Modal, etc.)
            3. Pages for each feature
            4. AuthContext for authentication
            5. API service layer
            6. Config files (package.json, vite.config.js, tailwind.config.js)
            
            Output as JSON with keys: app, components (dict), pages (dict), contexts (dict), services, config (dict)
            """,
            agent=self.agents['frontend'],
            expected_output="JSON with all frontend code",
            context=[pm_task, backend_task]
        )
        
        # Task 5: Testing
        qa_task = Task(
            description="""Write comprehensive test suites.
            
            Create:
            1. Backend tests (pytest) - auth tests, model tests
            2. Frontend tests (Vitest) - component tests, page tests
            3. E2E tests (Playwright) - user flow tests
            4. Test fixtures and utilities
            
            Output as JSON with keys: backend (dict), frontend (dict), e2e (dict)
            """,
            agent=self.agents['qa'],
            expected_output="JSON with all test files",
            context=[backend_task, frontend_task]
        )
        
        # Task 6: Deployment Setup
        devops_task = Task(
            description="""Setup production deployment configurations.
            
            Create:
            1. Backend Dockerfile
            2. Frontend Dockerfile
            3. docker-compose.yml (backend, frontend, database)
            4. GitHub Actions CI/CD workflow
            5. .env.example files
            6. .dockerignore
            
            Output as JSON with keys: docker (dict with dockerfiles, compose), ci_cd, env
            """,
            agent=self.agents['devops'],
            expected_output="JSON with deployment configs",
            context=[pm_task]
        )
        
        # Task 7: Documentation
        writer_task = Task(
            description="""Create comprehensive documentation.
            
            Create:
            1. README.md - Project overview, setup, usage
            2. API.md - API endpoints documentation
            3. ARCHITECTURE.md - System architecture
            4. SETUP.md - Detailed setup instructions
            5. CONTRIBUTING.md - Contribution guidelines
            6. TROUBLESHOOTING.md - Common issues and solutions
            
            Output as JSON with keys: readme, api, architecture, setup, contributing, troubleshooting
            """,
            agent=self.agents['writer'],
            expected_output="JSON with all documentation",
            context=[pm_task, backend_task, frontend_task]
        )
        
        return [pm_task, db_task, backend_task, frontend_task, qa_task, devops_task, writer_task]
    
    def build_application(self, user_requirements: str):
        """Build application using CrewAI framework"""
        
        start_time = datetime.now()
        
        print("\n" + "="*70)
        print("🚀 AUTODEV - AI FULL-STACK DEVELOPMENT TEAM (CrewAI)")
        print("="*70)
        print(f"\n📝 Requirements: {user_requirements}\n")
        
        try:
            # Create tasks
            tasks = self._create_tasks(user_requirements)
            
            # Create crew with sequential process
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the crew
            print("\n🎯 Starting CrewAI execution...\n")
            result = crew.kickoff()
            
            # Parse results from each task
            self._parse_crew_results(tasks)
            
            # Save project to disk
            execution_time = (datetime.now() - start_time).total_seconds()
            app_name = self.project_data.get('pm_spec', {}).get('app_name', 'generated-app')
            
            project_path = save_project_to_disk(
                project_data=self.project_data,
                app_name=app_name,
                output_base_dir="output/projects"
            )
            
            # Print summary
            self._print_summary(execution_time, project_path)
            
            return {
                'success': True,
                'project_path': str(project_path),
                'execution_time': execution_time
            }
            
        except Exception as e:
            logger.error(f"Build failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _parse_crew_results(self, tasks):
        """Parse results from CrewAI tasks"""
        
        try:
            # Parse each task output
            pm_output = self._parse_json_output(tasks[0].output.raw_output)
            db_output = self._parse_json_output(tasks[1].output.raw_output)
            backend_output = self._parse_json_output(tasks[2].output.raw_output)
            frontend_output = self._parse_json_output(tasks[3].output.raw_output)
            qa_output = self._parse_json_output(tasks[4].output.raw_output)
            devops_output = self._parse_json_output(tasks[5].output.raw_output)
            writer_output = self._parse_json_output(tasks[6].output.raw_output)
            
            # Store in project_data
            self.project_data = {
                'pm_spec': pm_output,
                'db_schema': db_output,
                'backend': backend_output,
                'frontend': frontend_output,
                'tests': qa_output,
                'deployment': devops_output,
                'documentation': writer_output
            }
            
        except Exception as e:
            logger.error(f"Failed to parse results: {str(e)}")
    
    def _parse_json_output(self, output: str) -> dict:
        """Parse JSON from agent output"""
        try:
            # Try to find JSON in output
            import re
            json_match = re.search(r'\{.*\}', output, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except:
            return {}
    
    def _print_summary(self, execution_time: float, project_path: Path):
        """Print execution summary"""
        
        pm_spec = self.project_data.get('pm_spec', {})
        
        print("\n" + "="*70)
        print("🎉 PROJECT BUILD COMPLETE!")
        print("="*70)
        print(f"""
📊 PROJECT DETAILS:
  • Name: {pm_spec.get('app_name', 'N/A')}
  • Type: {pm_spec.get('app_type', 'N/A')}
  • Time: {execution_time:.1f} seconds ({execution_time/60:.1f} minutes)

📁 PROJECT LOCATION:
  • {project_path}

🚀 NEXT STEPS:
  1. cd {project_path}
  2. Setup .env files
  3. docker-compose up -d
  4. Access at http://localhost:3000

✅ All 7 agents completed using CrewAI framework!
        """)


def main():
    """Main entry point"""
    
    # Get user input
    print("\n" + "="*70)
    print("🤖 AUTODEV - CrewAI Framework")
    print("="*70)
    user_input = input("\n📝 Enter your application requirements: ").strip()
    
    if not user_input:
        user_input = "Build a todo list app with priorities and due dates"
        print(f"\n💡 Using example: {user_input}")
    
    # Create crew and build
    crew = AutoDevCrew()
    result = crew.build_application(user_input)
    
    if result['success']:
        print(f"\n✨ Build complete! Project saved to: {result['project_path']}\n")
    else:
        print(f"\n❌ Build failed: {result.get('error')}\n")


if __name__ == "__main__":
    main()
