import ast
import py_compile

FILE_PATH = "./generated_video.py"


import ast
from pyflakes import reporter
from pyflakes import api
import io

def validate_manim_code(generated_code):
    # 1. First pass: Check for SyntaxErrors (which you are already doing)
    try:
        ast.parse(generated_code)
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"

    # 2. Second pass: Check for undefined variables/functions using Pyflakes
    warning_stream = io.StringIO()
    error_stream = io.StringIO()
    
    rep = reporter.Reporter(warning_stream, error_stream)
    
    # Pyflakes checks the AST tree for logical errors like NameErrors
    api.check(generated_code, "generated_manim_script.py", rep)
    
    warnings = warning_stream.getvalue()
    errors = error_stream.getvalue()
    
    if errors or "undefined name" in warnings:
        # Pyflakes categorizes undefined names as warnings in its stream, 
        # but for our use case, they are fatal errors.
        return False, f"Static Analysis Failed:\n{errors}{warnings}"
        
    return True, "Code is safe to render."

# Example Usage
with open(FILE_PATH, "r") as f:
    ai_code = f.read()

# Crucial Step: Prepend Manim imports before checking!
test_code =  ai_code 

is_valid, message = validate_manim_code(test_code)
print(message)