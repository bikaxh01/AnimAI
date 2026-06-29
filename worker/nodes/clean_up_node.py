import shutil
import os
from loguru import logger
from schema.state_schema import AgentState

from langchain_core.runnables.config import RunnableConfig
from services.project_service import project_service
from services.cloudinary_service import cloudinary_service
from schema.state_schema import VideoStatus

def clean_up_node(state: AgentState, config: RunnableConfig) -> dict:
    thread_id = config.get("configurable", {}).get("thread_id")
    if thread_id:
        status = VideoStatus.FAILED.value if getattr(state, "has_error", False) else VideoStatus.COMPLETED.value
        update_data = {"status": status}
        
        if getattr(state, "lesson_plan", None):
            lp = state.lesson_plan
            update_data["title"] = lp.get("title") if isinstance(lp, dict) else getattr(lp, "title", None)
            update_data["description"] = lp.get("description") if isinstance(lp, dict) else getattr(lp, "description", None)
        code_file = getattr(state, "code_path", "")
        if code_file and os.path.exists(code_file):
            uploaded_code_url = cloudinary_service.upload(code_file, resource_type="raw")
            if uploaded_code_url:
                update_data["code_file"] = uploaded_code_url
            else:
                update_data["code_file"] = code_file
            
        video_url = getattr(state, "final_video_path", "") or getattr(state, "video_path", "")
        if video_url and os.path.exists(video_url):
            uploaded_video_url = cloudinary_service.upload(video_url, resource_type="video")
            if uploaded_video_url:
                update_data["video_url"] = uploaded_video_url
            else:
                update_data["video_url"] = video_url
            
        project_service.update(thread_id, update_data)
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
