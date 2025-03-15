import logging
from ollama import chat
import json
from fastapi import HTTPException
import asyncio

logger = logging.getLogger(__name__)

class LLMHandler:
    """
    Handles sending prompts to an LLM using the Ollama Python library.
    The handler accepts a required prompt and an optional query response,
    which is formatted and appended to the prompt.
    """
    def __init__(self, model: str):
        """
        Initialize the handler with the model to use.
        
        Args:
            model (str): The name or identifier of the LLM model.
        """
        self.model = model

    def run_prompt(self, prompt: str, data: str = None) -> str:
        """
        Run the prompt against the LLM model.
        
        Args:
            prompt (str): The prompt to send to the model.
            data (str, optional): An data str to append to the prompt.
        
        Returns:
            str: The response from the LLM model.
        """
        if data:
            prompt += f"\n\n{data}"
        
        logger.info(f"Running prompt: {prompt}")
        
        response = chat(model=self.model, messages=[{"role": "user", "content": prompt}], stream=False).message.content
        
        logger.info(f"Response from model: {response}")
        
        try:
            response_json = json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {e}")
            raise HTTPException(status_code=500, detail="Failed to decode JSON response from model.")

        return response_json