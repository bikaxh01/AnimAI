from loguru import logger
import json
import os
from datetime import datetime
from schema.state_schema import VideoStatus, AgentState
from schema.code_generator.code_generator_schema import CodeGenerationSchema
from prompts.code_generator_prompt import CODE_GENERATOR_PROMPT
from services.llm_client import LLMService

llm_service = LLMService()

def code_generator_node(state: AgentState) -> dict:
    prompt = state.prompt if state.prompt else "Unknown Topic"
    logger.info(type(state))
    script_scenes = []
    if state.script:
        if isinstance(state.script, dict):
            script_scenes = state.script.get("scenes", [])
        else:
            script_scenes = getattr(state.script, "scenes", [])

    storyboard_scenes = []
    if state.storyboard:
        if isinstance(state.storyboard, dict):
            storyboard_scenes = state.storyboard.get("scenes", [])
        else:
            storyboard_scenes = getattr(state.storyboard, "scenes", [])

    combined_scenes = []
    length = max(len(script_scenes), len(storyboard_scenes))
    
    for i in range(length):
        scene_info = {}
        
        # Add script data
        if i < len(script_scenes):
            s_scene = script_scenes[i]
            if isinstance(s_scene, dict):
                scene_info["title"] = s_scene.get("title", f"Scene {i+1}")
                scene_info["narration"] = s_scene.get("narration", "")
            else:
                scene_info["title"] = getattr(s_scene, "title", f"Scene {i+1}")
                scene_info["narration"] = getattr(s_scene, "narration", "")
                
        # Add storyboard data
        if i < len(storyboard_scenes):
            sb_scene = storyboard_scenes[i]
            if isinstance(sb_scene, dict):
                scene_info["visuals_steps"] = sb_scene.get("visuals_steps", [])
                if "title" not in scene_info:
                    scene_info["title"] = sb_scene.get("title", f"Scene {i+1}")
            else:
                scene_info["visuals_steps"] = getattr(sb_scene, "visuals_steps", [])
                if "title" not in scene_info:
                    scene_info["title"] = getattr(sb_scene, "title", f"Scene {i+1}")
                    
        combined_scenes.append(scene_info)

    # Convert combined scenes to JSON string for the prompt
    scenes_data_str = json.dumps(combined_scenes, indent=2)

    # Construct prompt
    formatted_prompt = CODE_GENERATOR_PROMPT.replace("{{prompt}}", prompt).replace("{{scenes_data}}", scenes_data_str)
    
    logger.info("\n\n")
    
    logger.info(f"formatted_prompt: {formatted_prompt}")
    # Invoke LLM
    response = llm_service.invoke(formatted_prompt, CodeGenerationSchema)
    # response = llm_service.invoke("write code to print the sum of 2 number in py", CodeGenerationSchema)
    logger.info(response)
    # Log the response summary
    logger.info("--- Code Generator LLM Response ---")
    if response is None:
        logger.info("Error: LLM returned None.")
        summary = ""
        code = ""
    else:
        summary = getattr(response, "summary", "") if hasattr(response, "summary") else response.get("summary", "")
        code = getattr(response, "code", "") if hasattr(response, "code") else response.get("code", "")
        
    logger.info(summary)
    logger.info("-----------------------------------")
    
    # Write code to codes directory with timestamp
    file_path = ""
    if code:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_path = os.path.join("codes", timestamp)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "code.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        logger.info(f"Generated code written to {file_path}")
    
    return {
        "manim_code": code,
        "video_path": file_path,
        "status": VideoStatus.GENERATING_CODE.value
    }
