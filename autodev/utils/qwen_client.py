"""
Qwen3-Coder API Client
Wrapper for Qubrid AI Platform integration
"""

import httpx
import asyncio
from typing import Optional, Dict, Any, List
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()


class QwenCoderClient:
    """Client for Qwen3-Coder API via Qubrid AI Platform"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 120,
        max_retries: int = 3
    ):
        self.api_key = api_key or os.getenv("QUBRID_API_KEY")
        self.base_url = base_url or os.getenv("QUBRID_BASE_URL", "https://platform.qubrid.com/api/v1/qubridai")
        self.model = model or os.getenv("QWEN_MODEL", "Qwen/Qwen3-Coder-30B-A3B-Instruct")
        self.timeout = timeout
        self.max_retries = max_retries
        
        if not self.api_key:
            raise ValueError("QUBRID_API_KEY not found in environment variables")
        
        logger.info(f"Initialized QwenCoderClient with model: {self.model}")
    
    async def generate_code(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 4000,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate code using Qwen3-Coder API
        
        Args:
            prompt: User instruction for code generation
            system_prompt: System message to set context
            temperature: Sampling temperature (0.1-0.3 recommended for code)
            max_tokens: Maximum tokens in response
            conversation_history: Previous messages for context
        
        Returns:
            Generated code as string
        """
        if system_prompt is None:
            system_prompt = (
                "You are an expert software developer specializing in clean, "
                "production-ready code. Generate well-structured, documented, "
                "and best-practice code. Include proper error handling, type hints, "
                "and comments where necessary."
            )
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json=payload
                    )
                    response.raise_for_status()
                    
                    result = response.json()
                    
                    
                    # Handle the response format
                    if "choices" in result:
                        generated_text = result["choices"][0]["message"]["content"]
                    elif "message" in result:
                        generated_text = result["message"]["content"]
                    elif "content" in result:
                        generated_text = result["content"]
                    else:
                        logger.error(f"Unexpected response format: {result}")
                        raise ValueError(f"Cannot parse response: {result}")
                    
                    logger.success(
                        f"Generated {len(generated_text)} characters "
                        f"(tokens used: ~{result.get('usage', {}).get('total_tokens', 'unknown')})"
                    )
                    
                    return generated_text
            
            except httpx.TimeoutException:
                logger.warning(f"Timeout on attempt {attempt + 1}/{self.max_retries}")
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
            
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
                if e.response.status_code == 429:
                    logger.warning("Rate limited, waiting before retry...")
                    await asyncio.sleep(5)
                else:
                    raise
            
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(2)
        
        raise Exception("Max retries exceeded")
    
    async def generate_code_with_feedback(
        self,
        initial_prompt: str,
        validator_func: callable,
        max_iterations: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate code with iterative validation and refinement"""
        conversation = []
        current_prompt = initial_prompt
        
        for iteration in range(max_iterations):
            logger.info(f"Generation iteration {iteration + 1}/{max_iterations}")
            
            code = await self.generate_code(
                current_prompt,
                conversation_history=conversation,
                **kwargs
            )
            
            conversation.extend([
                {"role": "user", "content": current_prompt},
                {"role": "assistant", "content": code}
            ])
            
            is_valid, feedback = validator_func(code)
            
            if is_valid:
                logger.success(f"Code validated successfully on iteration {iteration + 1}")
                return {
                    "code": code,
                    "valid": True,
                    "iterations": iteration + 1,
                    "feedback": feedback
                }
            
            logger.warning(f"Validation failed: {feedback}")
            current_prompt = (
                f"The previous code had issues:\n{feedback}\n\n"
                f"Please fix these issues and regenerate the code."
            )
        
        logger.error("Max iterations reached without valid code")
        return {
            "code": code,
            "valid": False,
            "iterations": max_iterations,
            "feedback": feedback
        }
    
    async def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        """Generate code for multiple prompts concurrently"""
        tasks = [self.generate_code(prompt, **kwargs) for prompt in prompts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        outputs = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Prompt {i} failed: {str(result)}")
                outputs.append(f"# Generation failed: {str(result)}")
            else:
                outputs.append(result)
        
        return outputs


_client_instance = None

def get_qwen_client() -> QwenCoderClient:
    """Get or create singleton QwenCoderClient instance"""
    global _client_instance
    if _client_instance is None:
        _client_instance = QwenCoderClient()
    return _client_instance


async def test_client():
    """Test the Qwen3-Coder client"""
    client = QwenCoderClient()
    
    test_prompt = """
    Create a Python function that calculates the Fibonacci sequence up to n terms.
    Include:
    - Type hints
    - Docstring
    - Error handling for invalid inputs
    - Example usage
    """
    
    print("Testing Qwen3-Coder API...")
    result = await client.generate_code(test_prompt, max_tokens=1000)
    print("\n" + "="*50)
    print("Generated Code:")
    print("="*50)
    print(result)


if __name__ == "__main__":
    asyncio.run(test_client())