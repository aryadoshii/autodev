"""
Custom Qwen LLM Wrapper for CrewAI
Implements "Trojan Horse" Bypass to fix LiteLLM Provider Errors.
"""

import os
import httpx
from typing import Any, List, Optional
from loguru import logger
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration

class QwenLLM(ChatOpenAI):
    """
    Custom LLM that acts like GPT-4 to pass validation, 
    but calls Qwen3-Coder via Qubrid in reality.
    """
    
    def __init__(self, **kwargs):
        # Get credentials
        api_key = kwargs.get('api_key') or os.getenv("QUBRID_API_KEY")
        if not api_key:
            raise ValueError("QUBRID_API_KEY not found")
            
        base_url = "https://platform.qubrid.com/api/v1/qubridai"
        
        # 1. THE TROJAN HORSE: We tell CrewAI this is "gpt-4"
        # This satisfies LiteLLM/Pydantic validation so they don't crash.
        super().__init__(
            openai_api_key=api_key,
            openai_api_base=base_url,
            model="gpt-4",  # <--- FAKE MODEL NAME TO PASS VALIDATION
            temperature=0.2,
            max_tokens=4000,
            tiktoken_model_name="gpt-4",
            **kwargs
        )
        
        # Store real credentials and model
        self.qubrid_api_key = api_key
        self.qubrid_base_url = base_url
        self.real_model_name = "Qwen/Qwen3-Coder-30B-A3B-Instruct"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        """
        Override generation to use HTTPX with the REAL model name.
        """
        # Format messages for Qubrid/OpenAI format
        formatted_messages = []
        for msg in messages:
            role = "user"
            if isinstance(msg, SystemMessage):
                role = "system"
            elif isinstance(msg, HumanMessage):
                role = "user"
            elif msg.type == "ai":
                role = "assistant"
            
            formatted_messages.append({"role": role, "content": msg.content})

        # Construct Payload with the REAL model
        payload = {
            "model": self.real_model_name, # <--- USING REAL MODEL HERE
            "messages": formatted_messages,
            "temperature": 0.2,
            "max_tokens": 4000,
            "stream": False
        }

        try:
            # Direct HTTP call to bypass LiteLLM bugs
            with httpx.Client(timeout=120.0) as client:
                response = client.post(
                    f"{self.qubrid_base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.qubrid_api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ API Error {response.status_code}: {response.text}")
                    raise ValueError(f"Qubrid API Error: {response.text}")
                
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Return standard LangChain result
                generation = ChatGeneration(
                    message=BaseMessage(content=content, type="ai")
                )
                return ChatResult(generations=[generation])

        except Exception as e:
            logger.error(f"❌ Generation Failed: {str(e)}")
            raise e