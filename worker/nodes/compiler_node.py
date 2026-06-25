from loguru import logger
import os
import subprocess
from schema.state_schema import VideoStatus, AgentState

def compiler_node(state: AgentState) -> dict:
    logger.info(f"--- Compiler Node ---")
    video_path = getattr(state, "video_path", "")
    
    if video_path:
        logger.info(f"Compiling Manim code at {video_path}...")
        try:
            media_dir = os.path.dirname(video_path)
            subprocess.run(["manim", "-qh", video_path, "VideoLesson", "--media_dir", media_dir], check=True, capture_output=True, text=True)
            logger.info("Compilation completed.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Compilation failed: {e.stderr}")
            return {
                "has_error": True,
                "compile_error": [f"Compilation Error:\n{e.stderr}"],
                "status": VideoStatus.COMPILING.value
            }
    else:
        logger.warning("No video_path found in state to compile.")
        
    logger.info("---------------------")
    
    return {
        "status": VideoStatus.COMPILING.value
    }
