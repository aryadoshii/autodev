"""
Custom Qwen LLM Wrapper for CrewAI (Fixed for v0.63+)
Integrates Qwen3-Coder-30B via Qubrid API
"""

from langchain.llms.base import LLM
from typing import Optional, List, Any, Mapping
import httpx
import os
from loguru import logger


class QwenLLM(LLM):
    """Custom LLM wrapper for Qwen3-Coder via Qubrid API"""
    
    # Define as regular attributes, not Pydantic Fields
    api_key: str
    base_url: str = "https://api.qubrid.ai/v1"
    model_name: str = "Qwen/Qwen3-Coder-30B-A3B-Instruct"
    temperature: float = 0.2
    max_tokens: int = 4000
    
    def __init__(self, **kwargs):
        # Get API key from env if not provided
        if 'api_key' not in kwargs:
            kwargs['api_key'] = os.getenv("QUBRID_API_KEY")
        
        # Set defaults
        kwargs.setdefault('base_url', "https://api.qubrid.ai/v1")
        kwargs.setdefault('model_name', "Qwen/Qwen3-Coder-30B-A3B-Instruct")
        kwargs.setdefault('temperature', 0.2)
        kwargs.setdefault('max_tokens', 4000)
        
        super().__init__(**kwargs)
    
    @property
    def _llm_type(self) -> str:
        return "qwen-coder"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """Call Qwen API"""
        
        try:
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Qwen3-Coder, an expert code generation assistant. Generate clean, production-ready code with proper documentation. Always output valid JSON when requested."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stream": False
            }
            
            with httpx.Client(timeout=120.0) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                generated_text = result["choices"][0]["message"]["content"]
                
                logger.success(f"✅ Generated {len(generated_text)} characters")
                return generated_text
                
        except Exception as e:
            logger.error(f"❌ Qwen API call failed: {str(e)}")
            raise
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Return identifying parameters"""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "base_url": self.base_url
        }