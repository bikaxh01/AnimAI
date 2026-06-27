from loguru import logger
from schema.state_schema import AgentState

CLEAN_UP_NODE = "clean_up_node"
DEBUG_NODE = "debug_node"
COMPILER_NODE = "compiler_node"

def route_after_validation(state: AgentState) -> str:
    if state.has_error:
        if getattr(state, "debug_attempts", 0) >= 5:
            logger.error("Max debug attempts reached. Ending graph.")
            return CLEAN_UP_NODE
        return DEBUG_NODE
    return COMPILER_NODE

def route_after_compilation(state: AgentState) -> str:
    if state.has_error:
        if getattr(state, "debug_attempts", 0) >= 5:
            logger.error("Max debug attempts reached during compilation. Ending graph.")
            return CLEAN_UP_NODE
        return DEBUG_NODE
    return CLEAN_UP_NODE
