from loguru import logger
import subprocess
import sys
from pydantic import BaseModel
from pathlib import Path
from services.llm_client import LLMService

sys.stdout.reconfigure(encoding='utf-8')

llm_service = LLMService()

class Answer(BaseModel):
    code: str
    summary: float
    className:str

def main():

    logger.info("Processing...\n")
    topic  = "Make video on Binary search explain using go lang"
    res = llm_service.invoke(f"""
    YOU ARE A HELPFUL ASSISTANT. YOUR TASK IS TO GENERATE MANIM CODE FOR THE GIVEN TOPIC.
    MAKE SURE THE CODE IS BUG-FREE AND COMPATIBLE WITH MANIM COMMUNITY VERSION.
    
    IMPORTANT CONSTRAINTS:
    1. DO NOT USE LaTeX (no Tex, no MathTex). LaTeX is NOT installed on the host system, so using Tex or MathTex will cause a crash. Instead:
       - Use plain Text or MarkupText for all text, math formulas, equations, and mathematical variables.
       - Use plain text representation for math symbols, e.g., "mid = (low + high) / 2" instead of LaTeX fractions.
    2. Displaying Code:
       - When using the Code mobject, use the `code_string` parameter (e.g., `Code(code_string=go_code_str, language="go")`).
       - Do NOT use the `code` parameter in the Code constructor, as it is invalid.
       - Do NOT use parameters like `style`, `line_no_from`, `formatter`, `font`, or `font_size` directly in the Code constructor, as they will cause TypeErrors. If styling is needed, use `formatter_style` for the style name (e.g., `formatter_style="monokai"`), and `line_numbers_from` instead of `line_no_from`.
    3. The approximate video length should be above 5 minutes.
    
    TOPIC:
    {topic}
    """)
  
    generated_code  = res.code
    className  = res.className
    summary = res.summary
    
    logger.info(f"\n\nSummary: {summary}")
    logger.info(f"\n \n Generated Code: {generated_code}")
     


    logger.info("Writing to file ")
    Path("generated_video.py").write_text(
    generated_code,
    encoding="utf-8"
   )


    result = subprocess.run(
    [
        "manim",
        "-qh",
        "generated_video.py",
        className
    ],
    capture_output=True,
    text=True
    )

    logger.info(result.stdout)
    logger.info(result.stderr)

    if result.returncode != 0:
        logger.info("Render failed")


if __name__ == "__main__":
    pass
    # main()
