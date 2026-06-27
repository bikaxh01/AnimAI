import shutil
import os
from loguru import logger
from schema.state_schema import AgentState

from langchain_core.runnables.config import RunnableConfig
def clean_up_node(state: AgentState, config: RunnableConfig) -> dict:
    thread_id = config.get("configurable", {}).get("thread_id")
    logger.info("--- Clean Up Node ---")
    code_path = getattr(state, "code_path", "")
    
    if code_path:
        dir_path = os.path.dirname(code_path)
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                logger.info(f"Deleted folder {dir_path}")
            except Exception as e:
                logger.error(f"Failed to delete {dir_path}: {e}")
        else:
            logger.info(f"Folder {dir_path} does not exist.")
    else:
        logger.warning("No code_path found in state to clean up.")
        
    logger.info("---------------------")
    return {}
