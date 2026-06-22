from schema.state_schema import VideoStatus, AgentState
from schema.lesson_planner.lesson_planner_schema import LessonPlannerSchema
from prompts.lesson_planner_prompt import LESSON_PLANNER_PROMPT
from services.llm_client import LLMService

llm_service = LLMService()

def lesson_planner_node(state: AgentState) -> dict:

    
    # 1. Get the prompt from the state
    prompt = state.prompt if state.prompt else "Unknown Topic"
    
    # 2. Construct the prompt by replacing {{prompt}} with the state prompt
    formatted_prompt = LESSON_PLANNER_PROMPT.replace("{{prompt}}", prompt)
    
    # 3. Invoke the LLM with the prompt and the output schema
    response = llm_service.invoke(formatted_prompt, LessonPlannerSchema)
    
    # 4. Log the response
    print("--- Lesson Planner LLM Response ---")
    print(response)
    print("-----------------------------------")
    
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
