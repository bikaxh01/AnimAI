import os
from schema.state_schema import VideoStatus, AgentState

def compiler_node(state: AgentState) -> dict:
    code = state.manim_code if state.manim_code else ""
    
    filename = "generated_video.py"
    
    # Write the code to a .py file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
        
    print(f"--- Compiler Node ---")
    print(f"Saved Manim code to {filename} (compilation skipped for now).")
    print("---------------------")
    
    return {
        "video_path": filename,
        "status": VideoStatus.COMPILING.value
    }
