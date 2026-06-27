import os
import json
from loguru import logger
from config.settings import settings
from schema.state_schema import VideoStatus, AgentState
from schema.script_writer.script_writer_schema import ScriptSchema
from prompts.script_writer_prompt import SCRIPT_WRITER_PROMPT
from services.llm_client import LLMService

llm_service = LLMService()

from langchain_core.runnables.config import RunnableConfig
from services.project_service import project_service
from schema.state_schema import VideoStatus
def script_writer_node(state: AgentState, config: RunnableConfig) -> dict:
    thread_id = config.get("configurable", {}).get("thread_id")
    if thread_id:
        project_service.update(thread_id, {"status": VideoStatus.WRITING_SCRIPT.value})
    if settings.ENV == "DEV":
        try:
            with open("dummy.json", "r", encoding="utf-8") as f:
                dummy_data = json.load(f)
            return {
                "script": dummy_data.get("script", {}),
                "status": VideoStatus.WRITING_SCRIPT.value
            }
        except Exception as e:
            logger.error(f"Failed to load dummy.json: {e}")

    # 1. Get prompt and lesson plan from the state
    prompt = state.prompt if state.prompt else "Unknown Topic"
    lesson_plan = state.lesson_plan if state.lesson_plan else {}
    
    # 2. Construct the prompt
    formatted_prompt = SCRIPT_WRITER_PROMPT.replace("{{prompt}}", prompt).replace("{{lesson_plan}}", str(lesson_plan))
    
    # 3. Invoke LLM with the prompt and the output schema
    response = llm_service.invoke(formatted_prompt, ScriptSchema)
    
    # 4. Log the response
    logger.info("--- Script Writer LLM Response ---")
    logger.info(response)
    logger.info("----------------------------------")
    
    # 5. Return updated state
    if response is None:
        return {
            "script": {},
            "status": VideoStatus.FAILED.value
        }
        
    return {
        "script": response.model_dump() if hasattr(response, "model_dump") else response.dict(),
        "status": VideoStatus.WRITING_SCRIPT.value
    }
