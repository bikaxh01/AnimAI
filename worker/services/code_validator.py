import ast
from pyflakes import reporter
from pyflakes import api
import io
import manim  # We need this to check real Manim functions

def validate_manim_code(generated_code):
    # 1. First pass: Check for SyntaxErrors and build the AST tree
    try:
        tree = ast.parse(generated_code)
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"

    # 2. NEW PASS: Verify explicit Manim imports against the actual library
    valid_manim_names = set(dir(manim))
    fake_imports = set()
    
    for node in ast.walk(tree):
        # Catch: from manim import FakeFunction
        if isinstance(node, ast.ImportFrom) and node.module == 'manim':
            for alias in node.names:
                if alias.name != '*' and alias.name not in valid_manim_names:
                    fake_imports.add(alias.name)
                    
    if fake_imports:
        return False, f"Code Rejected: The AI tried to import fake Manim functions: {fake_imports}"

    # 3. Third pass: Check for undefined variables using Pyflakes
    warning_stream = io.StringIO()
    error_stream = io.StringIO()
    
    rep = reporter.Reporter(warning_stream, error_stream)
    api.check(generated_code, "generated_manim_script.py", rep)
    
    raw_warnings = warning_stream.getvalue()
    errors = error_stream.getvalue()
    
    # FILTERING LOGIC: Silence unused imports and variables
    fatal_warnings = []
    
    # Add valid Manim constants you want Pyflakes to ignore if using `from manim import *`
    valid_constants = [  "'LEFT'", "'RIGHT'", "'UP'", "'ORIGIN'"]
    
    for line in raw_warnings.splitlines():
        if "undefined name" in line:
            is_constant = any(constant in line for constant in valid_constants)
            if not is_constant:
                fatal_warnings.append(line)
            
    filtered_warnings_str = "\n".join(fatal_warnings)
    
    if errors or filtered_warnings_str:
        return False, f"Static Analysis Failed:\n{errors}\n{filtered_warnings_str}"
        
    return True, "Code is safe to render."
