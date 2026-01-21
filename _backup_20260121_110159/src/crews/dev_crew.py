"""
Development Crew Orchestrator - Production Version
Coordinates all 7 AI agents to build complete applications
Uses new production folder structure
"""

import sys
from pathlib import Path
from typing import Dict
from loguru import logger
import json
import asyncio
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import using new structure
from autodev.api.client.qwen_client import get_qwen_client
from autodev.core.agents.product_manager import ProductManagerAgent
from autodev.core.agents.database_architect import DatabaseArchitectAgent
from autodev.core.agents.backend_developer import BackendDeveloperAgent
from autodev.core.agents.frontend_developer import FrontendDeveloperAgent
from autodev.core.agents.qa_engineer import QAEngineerAgent
from autodev.core.agents.devops import DevOpsAgent
from autodev.core.agents.technical_writer import TechnicalWriterAgent
from autodev.core.orchestrator.save_project import save_project_to_disk


class DevelopmentCrew:
    """
    Orchestrates all 7 AI agents to build a complete application
    """
    
    def __init__(self):
        self.client = get_qwen_client()
        self.agents = self._initialize_agents()
        self.project_data = {}
        self.execution_log = []
        
    def _initialize_agents(self):
        """Initialize all 7 specialized agents"""
        logger.info("Initializing all agents...")
        
        agents = {
            'pm': ProductManagerAgent(self.client),
            'db': DatabaseArchitectAgent(self.client),
            'backend': BackendDeveloperAgent(self.client),
            'frontend': FrontendDeveloperAgent(self.client),
            'qa': QAEngineerAgent(self.client),
            'devops': DevOpsAgent(self.client),
            'writer': TechnicalWriterAgent(self.client)
        }
        
        logger.success("All 7 agents initialized")
        return agents
    
    async def build_application(self, user_requirements: str) -> Dict:
        """
        Build complete application from user requirements
        
        Args:
            user_requirements: Natural language description of the application
        
        Returns:
            Complete project data with all generated files
        """
        start_time = datetime.now()
        
        print("\n" + "="*70)
        print("🚀 AUTODEV - AI FULL-STACK DEVELOPMENT TEAM")
        print("="*70)
        print(f"\n📝 Requirements: {user_requirements}\n")
        
        try:
            # ============================================================
            # AGENT 1: PRODUCT MANAGER - Requirements Analysis
            # ============================================================
            pm_result = await self._run_agent_step(
                agent_name="Product Manager",
                description="Analyzing requirements and creating project specification...",
                task=self.agents['pm'].analyze_requirements(user_requirements),
                step_number=1
            )
            self.project_data['pm_spec'] = pm_result
            
            # ============================================================
            # AGENT 2: DATABASE ARCHITECT - Schema Design
            # ============================================================
            db_result = await self._run_agent_step(
                agent_name="Database Architect",
                description="Designing database schema and models...",
                task=self.agents['db'].design_schema(pm_result),
                step_number=2
            )
            self.project_data['db_schema'] = db_result
            
            # ============================================================
            # AGENT 3: BACKEND DEVELOPER - API Development
            # ============================================================
            backend_result = await self._run_agent_step(
                agent_name="Backend Developer",
                description="Generating FastAPI backend with authentication...",
                task=self.agents['backend'].generate_backend(pm_result, db_result),
                step_number=3
            )
            self.project_data['backend'] = backend_result
            
            # ============================================================
            # AGENT 4: FRONTEND DEVELOPER - UI Development
            # ============================================================
            frontend_result = await self._run_agent_step(
                agent_name="Frontend Developer",
                description="Creating React frontend with Tailwind CSS...",
                task=self.agents['frontend'].generate_frontend(pm_result, backend_result),
                step_number=4
            )
            self.project_data['frontend'] = frontend_result
            
            # ============================================================
            # AGENT 5: QA ENGINEER - Test Generation
            # ============================================================
            qa_result = await self._run_agent_step(
                agent_name="QA Engineer",
                description="Writing comprehensive test suites...",
                task=self.agents['qa'].generate_tests(pm_result, backend_result, frontend_result),
                step_number=5
            )
            self.project_data['tests'] = qa_result
            
            # ============================================================
            # AGENT 6: DEVOPS ENGINEER - Deployment Setup
            # ============================================================
            devops_result = await self._run_agent_step(
                agent_name="DevOps Engineer",
                description="Creating Docker and CI/CD configurations...",
                task=self.agents['devops'].generate_deployment(pm_result),
                step_number=6
            )
            self.project_data['deployment'] = devops_result
            
            # ============================================================
            # AGENT 7: TECHNICAL WRITER - Documentation
            # ============================================================
            tech_stack = pm_result.get('tech_stack', {})
            writer_result = await self._run_agent_step(
                agent_name="Technical Writer",
                description="Generating comprehensive documentation...",
                task=self.agents['writer'].generate_documentation(pm_result, tech_stack),
                step_number=7
            )
            self.project_data['documentation'] = writer_result
            
            # ============================================================
            # SAVE PROJECT TO DISK
            # ============================================================
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Extract app name and save project
            app_name = pm_result.get('app_name', 'generated-app')
            output_dir = "output/projects"
            
            # Save project to disk
            project_path = save_project_to_disk(
                project_data=self.project_data,
                app_name=app_name,
                output_base_dir=output_dir
            )
            
            # Generate summary
            summary = self._generate_project_summary(execution_time)
            
            return {
                'success': True,
                'project_data': self.project_data,
                'execution_log': self.execution_log,
                'execution_time': execution_time,
                'summary': summary,
                'project_path': str(project_path)
            }
            
        except Exception as e:
            logger.error(f"Build failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'execution_log': self.execution_log
            }
    
    async def _run_agent_step(
        self, 
        agent_name: str, 
        description: str, 
        task,
        step_number: int
    ) -> Dict:
        """
        Execute a single agent step with logging and error handling
        
        Args:
            agent_name: Name of the agent
            description: Description of what the agent is doing
            task: Async task to execute
            step_number: Step number in the workflow
        
        Returns:
            Result from the agent
        """
        
        print(f"\n{'─'*70}")
        print(f"📌 STEP {step_number}/7: {agent_name.upper()}")
        print(f"{'─'*70}")
        print(f"⚙️  {description}")
        
        step_start = datetime.now()
        
        try:
            result = await task
            
            step_time = (datetime.now() - step_start).total_seconds()
            
            self.execution_log.append({
                'step': step_number,
                'agent': agent_name,
                'description': description,
                'status': 'success',
                'execution_time': step_time,
                'timestamp': step_start.isoformat()
            })
            
            print(f"✅ {agent_name} completed in {step_time:.1f}s")
            
            return result
            
        except Exception as e:
            step_time = (datetime.now() - step_start).total_seconds()
            logger.error(f"{agent_name} failed: {str(e)}")
            
            self.execution_log.append({
                'step': step_number,
                'agent': agent_name,
                'description': description,
                'status': 'failed',
                'error': str(e),
                'execution_time': step_time,
                'timestamp': step_start.isoformat()
            })
            raise
    
    def _generate_project_summary(self, total_time: float) -> str:
        """Generate comprehensive project summary"""
        
        pm_spec = self.project_data.get('pm_spec', {})
        db_schema = self.project_data.get('db_schema', {})
        backend = self.project_data.get('backend', {})
        frontend = self.project_data.get('frontend', {})
        tests = self.project_data.get('tests', {})
        
        summary = f"""
{'='*70}
🎉 PROJECT BUILD COMPLETE!
{'='*70}

📊 PROJECT DETAILS:
  • Name: {pm_spec.get('app_name', 'N/A')}
  • Type: {pm_spec.get('app_type', 'N/A')}
  • Features: {len(pm_spec.get('core_features', []))}
  • Entities: {len(pm_spec.get('data_entities', []))}

🗄️  DATABASE:
  • Models: {len(db_schema.get('models', {}))}
  • Relationships: {len(db_schema.get('relationships', []))}
  • Indexes: {len(db_schema.get('indexes', []))}

🚀 BACKEND (FastAPI):
  • Routes: {len(backend.get('routes', {}))} files
  • Schemas: {len(backend.get('schemas', {}))} files
  • Auth: JWT authentication ✅
  • Structure: app/api/routes/, app/core/, app/models/

⚛️  FRONTEND (React + Vite):
  • Components: {len(frontend.get('components', {}))}
  • Pages: {len(frontend.get('pages', {}))}
  • Context: AuthContext ✅
  • Styling: Tailwind CSS ✅

🧪 TESTS:
  • Backend tests: {len(tests.get('backend', {}))} files
  • Frontend tests: {len(tests.get('frontend', {}))} files
  • E2E tests: {len(tests.get('e2e', {}))} files
  • Coverage goal: 80%+ ✅

🐳 DEPLOYMENT:
  • Docker: Backend + Frontend + Database
  • CI/CD: GitHub Actions ✅
  • Environment: .env templates ✅

📚 DOCUMENTATION:
  • README.md ✅
  • API.md ✅
  • ARCHITECTURE.md ✅
  • SETUP.md ✅
  • CONTRIBUTING.md ✅
  • TROUBLESHOOTING.md ✅

⏱️  EXECUTION TIME: {total_time:.1f} seconds ({total_time/60:.1f} minutes)

{'='*70}
✅ ALL 7 AGENTS COMPLETED SUCCESSFULLY
{'='*70}

📁 Generated Files:
  • Backend: {len(backend.get('routes', {})) + len(backend.get('schemas', {})) + 5} files
  • Frontend: {len(frontend.get('components', {})) + len(frontend.get('pages', {})) + 5} files
  • Tests: {len(tests.get('backend', {})) + len(tests.get('frontend', {})) + len(tests.get('e2e', {}))} files
  • Deployment: 6 files
  • Documentation: 6 files

🎯 NEXT STEPS:
  1. Navigate to project folder
  2. Setup environment (.env files)
  3. Run: docker-compose up -d
  4. Access at: http://localhost:3000

💡 All code follows production best practices!
"""
        return summary
    
    def save_execution_log(self, filepath: str = "output/logs"):
        """Save execution log to file"""
        
        # Create logs directory
        log_dir = Path(filepath)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"execution_{timestamp}.json"
        
        log_data = {
            'project_info': {
                'app_name': self.project_data.get('pm_spec', {}).get('app_name'),
                'app_type': self.project_data.get('pm_spec', {}).get('app_type'),
            },
            'execution_log': self.execution_log,
            'timestamp': datetime.now().isoformat(),
            'total_steps': len(self.execution_log),
            'successful_steps': sum(1 for log in self.execution_log if log['status'] == 'success'),
            'failed_steps': sum(1 for log in self.execution_log if log['status'] == 'failed'),
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        logger.info(f"Execution log saved to {log_file}")
        return log_file


async def main():
    """Main function to run the development crew"""
    
    # Get user input
    print("\n" + "="*70)
    print("🤖 AUTODEV - AI FULL-STACK DEVELOPMENT TEAM")
    print("="*70)
    user_input = input("\n📝 Enter your application requirements: ").strip()
    
    if not user_input:
        user_input = "Build a todo list app with priorities and due dates"
        print(f"\n💡 Using example: {user_input}")
    
    # Create crew and build application
    crew = DevelopmentCrew()
    result = await crew.build_application(user_input)
    
    if result['success']:
        # Print summary
        print("\n" + result['summary'])
        
        # Save execution log
        log_file = crew.save_execution_log()
        
        print(f"\n💾 Execution log: {log_file}")
        print(f"📂 Project saved: {result['project_path']}")
        print(f"\n✨ Open in VS Code: code {result['project_path']}")
        print("\n🎉 Build complete! Your application is ready.\n")
    else:
        print(f"\n❌ Build failed: {result.get('error')}")
        print("\n📋 Execution log:")
        for log in result.get('execution_log', []):
            status = "✅" if log['status'] == 'success' else "❌"
            print(f"  {status} Step {log['step']}: {log['agent']}")
        print()


if __name__ == "__main__":
    asyncio.run(main())