from schema.state_schema import VideoStatus, AgentState
from schema.script_writer.script_writer_schema import ScriptSchema
from prompts.script_writer_prompt import SCRIPT_WRITER_PROMPT
from services.llm_client import LLMService

llm_service = LLMService()

def script_writer_node(state: AgentState) -> dict:
    # 1. Get prompt and lesson plan from the state
    prompt = state.prompt if state.prompt else "Unknown Topic"
    lesson_plan = state.lesson_plan if state.lesson_plan else {}
    
    # 2. Construct the prompt
    formatted_prompt = SCRIPT_WRITER_PROMPT.replace("{{prompt}}", prompt).replace("{{lesson_plan}}", str(lesson_plan))
    
    # 3. Invoke LLM with the prompt and the output schema
    response = llm_service.invoke(formatted_prompt, ScriptSchema)
    
    # 4. Log the response
    print("--- Script Writer LLM Response ---")
    print(response)
    print("----------------------------------")
    
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
