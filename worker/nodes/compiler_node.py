from loguru import logger
import os
import subprocess
from schema.state_schema import VideoStatus, AgentState

from langchain_core.runnables.config import RunnableConfig
from services.project_service import project_service
from schema.state_schema import VideoStatus
def compiler_node(state: AgentState, config: RunnableConfig) -> dict:
    thread_id = config.get("configurable", {}).get("thread_id")
    if thread_id:
        project_service.update(thread_id, {"status": VideoStatus.COMPILING.value})
    logger.info(f"--- Compiler Node ---")
    code_path = getattr(state, "code_path", "")
    
    if code_path:
        logger.info(f"Compiling Manim code at {code_path}...")
        try:
            media_dir = os.path.dirname(code_path)
            process = subprocess.run(["manim", "-qh", code_path, "VideoLesson", "--media_dir", media_dir], check=False, capture_output=True, text=True)
            
            # Print command outputs
            if process.stdout:
                logger.info(f"Compiler Output:\n{process.stdout}")
            if process.stderr:
                logger.warning(f"Compiler Stderr:\n{process.stderr}")
                
            if process.returncode != 0:
                logger.error(f"Compilation failed with return code {process.returncode}")
                return {
                    "has_error": True,
                    "compile_error": [f"Compilation Error:\n{process.stderr}"],
                    "status": VideoStatus.COMPILING.value
                }
                
            logger.info("Compilation completed.")
            # Set the final video path
            video_file_path = os.path.join(media_dir, "videos", "code", "1080p60", "VideoLesson.mp4").replace("\\", "/")
            
            logger.info("---------------------")
            return {
                "video_path": video_file_path,
                "status": VideoStatus.COMPILING.value
            }
        except Exception as e:
            logger.error(f"Compilation exception: {str(e)}")
            return {
                "has_error": True,
                "compile_error": [f"Compilation Exception:\n{str(e)}"],
                "status": VideoStatus.COMPILING.value
            }
    else:
        logger.warning("No code_path found in state to compile.")
        
    logger.info("---------------------")
    
    return {
        "status": VideoStatus.COMPILING.value
    }
