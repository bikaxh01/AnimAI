from loguru import logger
import os
from schema.state_schema import VideoStatus, AgentState

def compiler_node(state: AgentState) -> dict:
    code = state.manim_code if state.manim_code else ""
    
    filename = "generated_video.py"
    
    # Write the code to a .py file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
        
    logger.info(f"--- Compiler Node ---")
    logger.info(f"Saved Manim code to {filename} (compilation skipped for now).")
    logger.info("---------------------")
    
    return {
        "video_path": filename,
        "status": VideoStatus.COMPILING.value
    }
