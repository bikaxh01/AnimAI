from openai.types.shared import reasoning_effort
from loguru import logger
from langchain_fireworks import ChatFireworks
from pydantic import BaseModel
from typing import Type
from config.settings import settings
from langchain_google_genai import ChatGoogleGenerativeAI


class LLMService:
    def __init__(self, model_name: str = "accounts/fireworks/models/deepseek-v4-pro"):
        self.llm = ChatFireworks(
            api_key=settings.OPENAI_API_KEY,
            max_tokens=50000,
            model=model_name,
            reasoning_effort="none",

        )
        # self.llm = ChatGoogleGenerativeAI(
        #     model="gemini-3-flash-preview",
        #     temperature=1.0,  # Gemini 3.0+ defaults to 1.0
        #     max_tokens=None,
        #     timeout=None,
        #     max_retries=2,
        #     api_key="",
        # )

    def invoke(self, prompt: str, output_schema: Type[BaseModel]):
        structured_output = self.llm.with_structured_output(
            output_schema,
        )
        try:
            return structured_output.invoke(prompt)
        except Exception as e:
            logger.error(f"LLM API Call Failed: {e}")
            return None
