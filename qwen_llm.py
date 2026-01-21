"""
Custom Qwen LLM Wrapper for CrewAI
Integrates Qwen3-Coder-30B via Qubrid API with CrewAI framework
"""

from langchain.llms.base import LLM
from typing import Optional, List, Any
import httpx
import os
from pydantic import Field
from loguru import logger


class QwenLLM(LLM):
    """Custom LLM wrapper for Qwen3-Coder via Qubrid API"""
    
    api_key: str = Field(default_factory=lambda: os.getenv("QUBRID_API_KEY"))
    base_url: str = Field(default="https://api.qubrid.ai/v1")
    model: str = Field(default="Qwen/Qwen3-Coder-30B-A3B-Instruct")
    temperature: float = Field(default=0.2)
    max_tokens: int = Field(default=4000)
    
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
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Qwen3-Coder, an expert code generation assistant. Generate clean, production-ready code with proper documentation."
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
                
                logger.success(f"Generated {len(generated_text)} characters")
                return generated_text
                
        except Exception as e:
            logger.error(f"Qwen API call failed: {str(e)}")
            return f"Error: {str(e)}"
    
    @property
    def _identifying_params(self) -> dict:
        """Return identifying parameters"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
