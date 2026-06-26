from loguru import logger
import os
from schema.state_schema import AgentState, VideoStatus
from schema.code_generator.code_generator_schema import CodeGenerationSchema
from prompts.debugger_prompt import DEBUGGER_PROMPT
from services.llm_client import LLMService

llm_service = LLMService()

def debug_node(state: AgentState) -> dict:
    logger.info("--- Debugger Node ---")
    
    error = state.compile_error[-1] if state.compile_error else "Unknown error"
    
    code_path = getattr(state, "code_path", "")
    code = ""
    if code_path and os.path.exists(code_path):
        with open(code_path, "r", encoding="utf-8") as f:
            code = f.read()
    else:
        code = state.manim_code if state.manim_code else ""
        
    formatted_prompt = DEBUGGER_PROMPT.replace("{{code}}", code).replace("{{error}}", error)
    
    response = llm_service.invoke(formatted_prompt, CodeGenerationSchema)
    
    if response is None:
        logger.error("Error: LLM returned None.")
        new_code = code
    else:
        new_code = getattr(response, "code", "") if hasattr(response, "code") else response.get("code", "")
        summary = getattr(response, "summary", "") if hasattr(response, "summary") else response.get("summary", "")
        logger.info(f"Debugger summary: {summary}")
        
    if new_code and code_path:
        with open(code_path, "w", encoding="utf-8") as f:
            f.write(new_code)
        logger.info(f"Updated code written to {code_path}")
        
    return {
        "manim_code": new_code,
        "has_error": False,
        "debug_attempts": getattr(state, "debug_attempts", 0) + 1,
        "status": VideoStatus.GENERATING_CODE.value
    }
