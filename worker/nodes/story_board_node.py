from schema.state_schema import VideoStatus, AgentState
from schema.storyboard.storyboard_schema import StoryboardSchema
from prompts.storyboard_prompt import STORYBOARD_PROMPT
from services.llm_client import LLMService

llm_service = LLMService()

def storyboard_node(state: AgentState) -> dict:
    # 1. Get script from the state
    script = state.script if state.script else {}
    
    # 2. Construct the prompt
    formatted_prompt = STORYBOARD_PROMPT.replace("{{script}}", str(script))
    
    # 3. Invoke LLM with the prompt and the output schema
    response = llm_service.invoke(formatted_prompt, StoryboardSchema)
    
    # 4. Log the response
    print("--- Storyboard LLM Response ---")
    print(response)
    print("-------------------------------")
    
    # 5. Return updated state
    if response is None:
        return {
            "storyboard": {},
            "status": VideoStatus.FAILED.value
        }
        
    return {
        "storyboard": response.model_dump() if hasattr(response, "model_dump") else response.dict(),
        "status": VideoStatus.STORYBOARDING.value
    }
