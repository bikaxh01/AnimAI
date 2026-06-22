from loguru import logger
from langchain_fireworks import ChatFireworks
from pydantic import BaseModel
from typing import Type
from config.settings import settings

class LLMService:
    def __init__(self,model_name:str = "accounts/fireworks/models/deepseek-v4-pro"):
        self.llm = ChatFireworks(
            api_key=settings.OPENAI_API_KEY,
            max_tokens=15000,
            model=model_name
        )

    def invoke(self, prompt: str, output_schema: Type[BaseModel]):
        structured_output = self.llm.with_structured_output(output_schema)
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            logger.error(f"LLM API Call Failed: {e}")
            return None


