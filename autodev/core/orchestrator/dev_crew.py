"""
Development Crew - CrewAI Framework with Qubrid API
Standard OpenAI Configuration for Qubrid
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
from langchain_openai import ChatOpenAI
from autodev.core.orchestrator.save_project import save_project_to_disk

class AutoDevCrew:
    """AutoDev Crew using CrewAI Framework"""
    
    def __init__(self):
        """Initialize with Standard ChatOpenAI for Qubrid"""
        
        api_key = os.getenv("QUBRID_API_KEY")
        if not api_key:
            raise ValueError("QUBRID_API_KEY not found")
            
        base_url = "https://platform.qubrid.com/api/v1/qubridai"
        
        # 1. SET ENVIRONMENT VARIABLES
        # This ensures LiteLLM (used by CrewAI) knows exactly where to look
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_API_BASE"] = base_url
        os.environ["OPENAI_MODEL_NAME"] = "Qwen/Qwen3-Coder-30B-A3B-Instruct"
        
        # 2. STANDARD CHATOPENAI CONFIGURATION
        # We use the 'openai/' prefix string here.
        # This tells CrewAI: "Use the OpenAI protocol (which Qubrid supports),
        # but ask for this specific Qwen model."
        self.llm = ChatOpenAI(
            model="openai/Qwen/Qwen3-Coder-30B-A3B-Instruct",
            api_key=api_key,
            base_url=base_url,
            temperature=0.2,
            max_tokens=4000
        )
        
        logger.info(f"✅ Configured Qwen3-Coder via Qubrid")
        
        self.agents = self._create_agents()
        self.project_data = {}
        
    def _create_agents(self):
        """Create agents using the configured LLM"""
        
        agent_config = {
            "llm": self.llm,
            "verbose": True,
            "allow_delegation": False
        }
        
        # Agent 1: Product Manager
        product_manager = Agent(
            role="Product Manager",
            goal="Analyze requirements and create technical specs",
            backstory="Expert Product Manager.",
            **agent_config
        )
        
        # Agent 2: Database Architect
        database_architect = Agent(
            role="Database Architect",
            goal="Design database schemas",
            backstory="Expert Database Architect.",
            **agent_config
        )
        
        # Agent 3: Backend Developer
        backend_developer = Agent(
            role="Backend Developer",
            goal="Build FastAPI backends",
            backstory="Expert Backend Developer.",
            **agent_config
        )
        
        # Agent 4: Frontend Developer
        frontend_developer = Agent(
            role="Frontend Developer",
            goal="Create React frontends",
            backstory="Expert Frontend Developer.",
            **agent_config
        )
        
        # Agent 5: QA Engineer
        qa_engineer = Agent(
            role="QA Engineer",
            goal="Write test suites",
            backstory="Expert QA Engineer.",
            **agent_config
        )
        
        # Agent 6: DevOps Engineer
        devops_engineer = Agent(
            role="DevOps Engineer",
            goal="Setup deployment pipelines",
            backstory="Expert DevOps Engineer.",
            **agent_config
        )
        
        # Agent 7: Technical Writer
        technical_writer = Agent(
            role="Technical Writer",
            goal="Create documentation",
            backstory="Expert Technical Writer.",
            **agent_config
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
        """Create tasks for each agent"""
        
        # Task 1: Requirements Analysis
        pm_task = Task(
            description=f"Analyze requirements: '{user_requirements}'. Output JSON with keys: app_name, app_type, core_features, data_entities, tech_stack.",
            agent=self.agents['pm'],
            expected_output="JSON specification"
        )
        
        # Task 2: Database Design
        db_task = Task(
            description="Design database schema based on PM spec. Output JSON with models.",
            agent=self.agents['db'],
            expected_output="JSON database schema",
            context=[pm_task]
        )
        
        # Task 3: Backend
        backend_task = Task(
            description="Generate FastAPI backend. Output JSON with main.py, routes, schemas.",
            agent=self.agents['backend'],
            expected_output="JSON backend code",
            context=[pm_task, db_task]
        )
        
        # Task 4: Frontend
        frontend_task = Task(
            description="Generate React frontend. Output JSON with components, pages.",
            agent=self.agents['frontend'],
            expected_output="JSON frontend code",
            context=[pm_task, backend_task]
        )
        
        # Task 5: QA
        qa_task = Task(
            description="Generate tests. Output JSON with test files.",
            agent=self.agents['qa'],
            expected_output="JSON tests",
            context=[backend_task, frontend_task]
        )
        
        # Task 6: DevOps
        devops_task = Task(
            description="Generate Docker/CI config. Output JSON with files.",
            agent=self.agents['devops'],
            expected_output="JSON deployment config",
            context=[pm_task]
        )
        
        # Task 7: Docs
        writer_task = Task(
            description="Generate README.md. Output JSON with documentation.",
            agent=self.agents['writer'],
            expected_output="JSON documentation",
            context=[pm_task, backend_task]
        )
        
        return [pm_task, db_task, backend_task, frontend_task, qa_task, devops_task, writer_task]
    
    def build_application(self, user_requirements: str):
        """Build application using CrewAI framework"""
        start_time = datetime.now()
        
        print("\n" + "="*70)
        print("🚀 AUTODEV - CrewAI + Qwen3-Coder")
        print("="*70)
        
        try:
            tasks = self._create_tasks(user_requirements)
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            print("\n🎯 Starting CrewAI execution...\n")
            crew.kickoff()
            
            self._parse_crew_results(tasks)
            app_name = self.project_data.get('pm_spec', {}).get('app_name', 'generated-app')
            project_path = save_project_to_disk(self.project_data, app_name, "output/projects")
            
            self._print_summary((datetime.now() - start_time).total_seconds(), project_path)
            return {'success': True, 'project_path': str(project_path)}
            
        except Exception as e:
            logger.error(f"Build failed: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _parse_crew_results(self, tasks):
        try:
            import re
            def extract_json(text):
                json_match = re.search(r'\{.*\}', text, re.DOTALL)
                return json.loads(json_match.group()) if json_match else {}
            
            self.project_data = {
                'pm_spec': extract_json(str(tasks[0].output)),
                'db_schema': extract_json(str(tasks[1].output)),
                'backend': extract_json(str(tasks[2].output)),
                'frontend': extract_json(str(tasks[3].output)),
                'tests': extract_json(str(tasks[4].output)),
                'deployment': extract_json(str(tasks[5].output)),
                'documentation': extract_json(str(tasks[6].output))
            }
        except:
            pass

    def _print_summary(self, time, path):
        print(f"\n✅ Done in {time:.1f}s at {path}")

def main():
    user_input = input("\n📝 Enter requirements: ").strip() or "Build a ludo game"
    crew = AutoDevCrew()
    crew.build_application(user_input)

if __name__ == "__main__":
    main()