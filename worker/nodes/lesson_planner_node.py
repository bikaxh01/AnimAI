import os
import json
from loguru import logger
from config.settings import settings
from schema.state_schema import VideoStatus, AgentState
from schema.lesson_planner.lesson_planner_schema import LessonPlannerSchema
from prompts.lesson_planner_prompt import LESSON_PLANNER_PROMPT
from services.llm_client import LLMService

llm_service = LLMService()

from langchain_core.runnables.config import RunnableConfig
from services.project_service import project_service
from schema.state_schema import VideoStatus
def lesson_planner_node(state: AgentState, config: RunnableConfig) -> dict:
    thread_id = config.get("configurable", {}).get("thread_id")
    if thread_id:
        project_service.update(thread_id, {"status": VideoStatus.PLANNING.value})
    if settings.ENV == "DEV":
        try:
            with open("dummy.json", "r", encoding="utf-8") as f:
                dummy_data = json.load(f)
            return {
                "lesson_plan": dummy_data.get("lesson_plan", {}),
                "status": VideoStatus.PLANNING.value
            }
        except Exception as e:
            logger.error(f"Failed to load dummy.json: {e}")


    
    # 1. Get the prompt from the state
    prompt = state.prompt if state.prompt else "Unknown Topic"
    
    # 2. Construct the prompt by replacing {{prompt}} with the state prompt
    formatted_prompt = LESSON_PLANNER_PROMPT.replace("{{prompt}}", prompt)
    
    # 3. Invoke the LLM with the prompt and the output schema
    response = llm_service.invoke(formatted_prompt, LessonPlannerSchema)
    
    # 4. Log the response
    logger.info("--- Lesson Planner LLM Response ---")
    logger.info(response)
    logger.info("-----------------------------------")
    
    # 5. Return updated state
    if response is None:
        return {
            "lesson_plan": {},
            "status": VideoStatus.FAILED.value
        }
        
    return {
        "lesson_plan": response.model_dump() if hasattr(response, "model_dump") else response.dict(),
        "status": VideoStatus.PLANNING.value
    }
