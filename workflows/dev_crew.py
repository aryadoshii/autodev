"""
Development Crew - CrewAI Framework with Qubrid API
FIXED VERSION: With Debugging + Better Parser
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import os
import re
import ast
import yaml
from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from crewai import Agent, Task, Crew, Process, LLM
from workflows.save_project import save_project_to_disk

class AutoDevCrew:
    """AutoDev Crew using CrewAI Framework"""
    
    def __init__(self):
        """Initialize with Native LLM for Qubrid"""
        
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_API_BASE")
        model_name = os.getenv("OPENAI_MODEL_NAME")

        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env")
            
        self.llm = LLM(
            model=model_name,
            base_url=base_url,
            api_key=api_key,
            stream=True
        )
        
        # Load Configurations
        self.agents_config = self._load_yaml('environment/agents.yaml')
        self.tasks_config = self._load_yaml('environment/tasks.yaml')
        
        self.agents = self._create_agents()
        self.project_data = {}

    def _load_yaml(self, relative_path):
        project_root = Path(__file__).parent.parent
        path = project_root / relative_path
        with open(path, 'r') as f:
            return yaml.safe_load(f)
        
    def _create_agents(self):
        """Create agents (Verbose=False for clean output)"""
        def create(role_name):
            config = self.agents_config[role_name]
            return Agent(
                role=config['role'],
                goal=config['goal'],
                backstory=config['backstory'],
                llm=self.llm,
                verbose=False,
                allow_delegation=False
            )
        
        return {
            'pm': create('product_manager'),
            'db': create('database_architect'),
            'backend': create('backend_developer'),
            'frontend': create('frontend_developer'),
            'qa': create('qa_engineer'),
            'devops': create('devops_engineer'),
            'writer': create('technical_writer')
        }
    
    def _create_tasks(self, user_requirements: str):
        """Create tasks with improved prompts"""
        def create(task_name, agent_key, context_tasks=None, **kwargs):
            config = self.tasks_config[task_name]
            
            # CRITICAL: Enhanced JSON instruction
            strict_instruction = """

CRITICAL OUTPUT FORMAT:
- Output MUST be valid JSON
- Use a flat dictionary: {"filename": "code content"}
- For code with newlines, use \\n explicitly
- Escape all quotes inside code with \\"
- Do NOT use nested structures
- Do NOT wrap in markdown code blocks

Example:
{
  "main.py": "from fastapi import FastAPI\\n\\napp = FastAPI()\\n\\n@app.get(\\"/\\")\\ndef read_root():\\n    return {\\"message\\": \\"Hello World\\"}"
}
"""
            
            description = config['description'].format(user_requirements=user_requirements) + strict_instruction
            
            return Task(
                description=description,
                expected_output=config['expected_output'],
                agent=self.agents[agent_key],
                context=context_tasks if context_tasks else [],
                **kwargs
            )
        
        # Define tasks
        pm_task = create('analysis_task', 'pm')
        db_task = create('db_design_task', 'db', [pm_task])
        backend_task = create('backend_task', 'backend', [pm_task, db_task])
        frontend_task = create('frontend_task', 'frontend', [pm_task, backend_task])
        qa_task = create('qa_task', 'qa', [backend_task, frontend_task])
        devops_task = create('devops_task', 'devops', [pm_task])
        writer_task = create('documentation_task', 'writer', [pm_task, backend_task])
        
        return [pm_task, db_task, backend_task, frontend_task, qa_task, devops_task, writer_task]
    
    def build_application(self, user_requirements: str):
        """Build application"""
        start_time = datetime.now()
        
        print("\n" + "="*70)
        print("🚀 AUTODEV - Starting Development Cycle")
        print("="*70)
        
        try:
            tasks = self._create_tasks(user_requirements)
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                process=Process.sequential,
                verbose=False
            )
            
            print("\n⏳ Agents are working... (This may take 2-3 minutes)")
            crew.kickoff()
            
            print("\n🛠️ Parsing and assembling project files...")
            print("="*70)
            self._parse_crew_results(tasks)
            
            # Debug: Print project_data summary
            print("\n📊 PARSING RESULTS:")
            for key, value in self.project_data.items():
                if isinstance(value, dict):
                    file_count = len(value)
                    files = list(value.keys())[:3]  # First 3 files
                    print(f"  ✅ {key}: {file_count} files ({', '.join(files)}...)")
                else:
                    print(f"  ⚠️  {key}: {type(value)} (expected dict)")
            print("="*70)
            
            # Check if we have any actual data
            total_files = sum(len(v) if isinstance(v, dict) else 0 for v in self.project_data.values())
            if total_files == 0:
                logger.error("❌ NO FILES PARSED! All agent outputs were empty or invalid.")
                return {'success': False, 'error': 'No files were generated'}
            
            # Determine App Name
            app_data = self.project_data.get('pm_spec', {})
            if isinstance(app_data, dict) and 'generated-file-0' in app_data:
                app_name = f'generated-app-{int(datetime.now().timestamp())}'
            else:
                app_name = app_data.get('app_name', f'generated-app-{int(datetime.now().timestamp())}')
            
            output_dir = "output/projects"
            os.makedirs(output_dir, exist_ok=True)

            # Around line 180, before save_project_to_disk()
            print("\n🔍 INSPECTING PROJECT DATA:")
            for section, data in self.project_data.items():
                if isinstance(data, dict):
                    print(f"  {section}: {len(data)} items")
                    for fname in list(data.keys())[:2]:
                        print(f"    - {fname}")
            
            # Save project
            project_path = save_project_to_disk(self.project_data, app_name, output_dir)
            
            self._print_summary((datetime.now() - start_time).total_seconds())
            return {'success': True, 'project_path': str(project_path)}
            
        except Exception as e:
            logger.error(f"Build failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {'success': False, 'error': str(e)}

    def _parse_crew_results(self, tasks):
        """
        IMPROVED Parser with Multi-Strategy Approach + Debugging
        """
        
        def clean_and_parse_json(text_output, agent_name="Unknown"):
            """Enhanced parser with detailed logging"""
            
            if not text_output:
                logger.warning(f"[{agent_name}] Empty output")
                return {}
            
            text = str(text_output).strip()
            
            # Log raw output (first 500 chars)
            logger.debug(f"[{agent_name}] Raw output preview: {text[:500]}...")
            
            # Strategy 1: Clean Markdown
            text = re.sub(r'```json\s*', '', text)
            text = re.sub(r'```\s*', '', text)
            text = text.strip()
            
            # Strategy 2: Standard JSON Parse
            try:
                result = json.loads(text)
                logger.success(f"[{agent_name}] ✅ Parsed with json.loads()")
                return self._ensure_dict(result)
            except json.JSONDecodeError as e:
                logger.warning(f"[{agent_name}] json.loads() failed: {e}")
            
            # Strategy 3: Try fixing common JSON issues
            try:
                # Fix unescaped newlines in strings (aggressive approach)
                # This regex tries to find content between quotes and escape newlines
                def fix_strings(match):
                    content = match.group(1)
                    # Escape newlines and quotes
                    fixed = content.replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '\\r')
                    return f'"{fixed}"'
                
                # Match strings between quotes (non-greedy)
                fixed_text = re.sub(r'"([^"\\]*(?:\\.[^"\\]*)*)"', fix_strings, text)
                result = json.loads(fixed_text)
                logger.success(f"[{agent_name}] ✅ Parsed after string fixing")
                return self._ensure_dict(result)
            except Exception as e:
                logger.warning(f"[{agent_name}] String fixing failed: {e}")
            
            # Strategy 4: ast.literal_eval (handles Python-style dicts)
            try:
                result = ast.literal_eval(text)
                logger.success(f"[{agent_name}] ✅ Parsed with ast.literal_eval()")
                return self._ensure_dict(result)
            except Exception as e:
                logger.warning(f"[{agent_name}] ast.literal_eval() failed: {e}")
            
            # Strategy 5: Regex extraction (last resort)
            logger.warning(f"[{agent_name}] Using regex extraction (last resort)")
            extracted = {}
            
            # Pattern 1: Match "filename.ext": "content"
            pattern1 = r'"([^"]+\.(py|js|jsx|tsx|ts|css|html|md|txt|yml|yaml|json|sh|dockerfile))"\s*:\s*"([^"]*(?:\\.[^"]*)*)"'
            matches = re.findall(pattern1, text, re.IGNORECASE | re.DOTALL)
            
            for filename, _, content in matches:
                # Unescape the content
                content = content.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\').replace('\\t', '\t')
                extracted[filename] = content
                logger.info(f"[{agent_name}] Extracted: {filename}")
            
            # Pattern 2: Try to find any key-value pairs
            if not extracted:
                pattern2 = r'[\"\']([^\"\']+)[\"\']:\s*[\"\']([^\"\']+)[\"\']'
                matches = re.findall(pattern2, text)
                for key, value in matches:
                    if '.' in key:  # Likely a filename
                        extracted[key] = value.replace('\\n', '\n')
            
            if not extracted:
                logger.error(f"[{agent_name}] ❌ ALL PARSING STRATEGIES FAILED")
                # Save the problematic output for debugging
                debug_file = f"debug_output_{agent_name}_{int(datetime.now().timestamp())}.txt"
                with open(debug_file, 'w') as f:
                    f.write(text)
                logger.error(f"[{agent_name}] Saved raw output to: {debug_file}")
            else:
                logger.info(f"[{agent_name}] Regex extracted {len(extracted)} files")
            
            return extracted

        # Parse each task output
        agent_names = ['Product Manager', 'Database Architect', 'Backend Dev', 
                       'Frontend Dev', 'QA Engineer', 'DevOps', 'Tech Writer']
        
        self.project_data = {}
        keys = ['pm_spec', 'db_schema', 'backend', 'frontend', 'tests', 'deployment', 'documentation']
        
        for i, (key, task, agent_name) in enumerate(zip(keys, tasks, agent_names)):
            print(f"\n🔍 Parsing {agent_name} output...")
            parsed = clean_and_parse_json(task.output, agent_name)
            self.project_data[key] = parsed
            
            # Validate
            if not parsed:
                logger.warning(f"⚠️  {agent_name} produced no valid output")
            elif not isinstance(parsed, dict):
                logger.warning(f"⚠️  {agent_name} output is not a dict: {type(parsed)}")
            else:
                logger.success(f"✅ {agent_name} produced {len(parsed)} files")

    def _ensure_dict(self, data):
        """Ensure data is a dict"""
        if isinstance(data, list):
            return {f"generated-file-{i}": item for i, item in enumerate(data)}
        if not isinstance(data, dict):
            return {}
        return data

    def _print_summary(self, time):
        print(f"\n✅ Execution completed in {time:.1f}s")

def main():
    user_input = input("\n📝 Enter requirements: ").strip() or "Build a simple todo app"
    crew = AutoDevCrew()
    result = crew.build_application(user_input)
    
    if not result['success']:
        print(f"\n❌ Build failed: {result['error']}")
    else:
        print(f"\n✅ Project saved to: {result['project_path']}")

if __name__ == "__main__":
    main()