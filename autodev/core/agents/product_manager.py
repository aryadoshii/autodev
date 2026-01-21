"""Product Manager Agent"""
import sys
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class ProductManagerAgent:
    def __init__(self, qwen_client):
        self.qwen_client = qwen_client
    
    async def analyze_requirements(self, user_input: str, tech_preferences: Optional[Dict] = None) -> Dict:
        logger.info("Starting requirements analysis...")
        
        prompt = f"""Analyze this user request and create a detailed software specification:

USER REQUEST: {user_input}

Output ONLY valid JSON with this structure:
{{
  "app_type": "Description",
  "app_name": "project-name",
  "description": "Summary",
  "core_features": ["Feature 1", "Feature 2"],
  "data_entities": [{{"name": "Entity", "attributes": ["attr1"]}}],
  "tech_stack": {{"backend": "FastAPI", "frontend": "React", "database": "PostgreSQL"}},
  "development_tasks": [
    {{"id": 1, "agent": "database", "task": "Design schema", "priority": "high"}}
  ]
}}"""
        
        response = await self.qwen_client.generate_code(
            prompt=prompt,
            system_prompt="You are an expert product manager. Output ONLY valid JSON.",
            temperature=0.3,
            max_tokens=3000
        )
        
        spec = self._parse_specification(response)
        logger.success(f"Requirements analyzed: {spec.get('app_type', 'Unknown')}")
        return spec
    
    def _parse_specification(self, response: str) -> Dict:
        response = response.strip()
        if response.startswith("```json"):
            response = response.split("```json")[1].split("```")[0].strip()
        elif response.startswith("```"):
            response = response.split("```")[1].split("```")[0].strip()
        return json.loads(response)

async def test_pm_agent():
    from src.utils.qwen_client import get_qwen_client
    
    client = get_qwen_client()
    pm_agent = ProductManagerAgent(client)
    
    test_input = "Build a task management app with user authentication"
    spec = await pm_agent.analyze_requirements(test_input)
    
    print("\n" + "="*60)
    print(json.dumps(spec, indent=2))
    print("="*60)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_pm_agent())