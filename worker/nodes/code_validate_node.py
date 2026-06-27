from loguru import logger
from schema.state_schema import AgentState
from services.code_validator import validate_manim_code

from langchain_core.runnables.config import RunnableConfig
def code_validate_node(state: AgentState, config: RunnableConfig) -> dict:
    thread_id = config.get("configurable", {}).get("thread_id")
    code = state.manim_code if state.manim_code else ""
    
    logger.info("--- Code Validate Node ---")
    
    is_valid, message = validate_manim_code(code)
    
    if is_valid:
        logger.info("Code validation passed.")
        # Return state as it is (no modifications to error state)
        return {}
    else:
        logger.info(f"Code validation failed: {message}")
        # Update state: append error to compile_error, set has_error to True
        current_errors = list(state.compile_error) if state.compile_error else []
        current_errors.append(message)
        
        return {
            "compile_error": current_errors,
            "has_error": True
        }
