from langgraph.graph import StateGraph, START, END
from nodes.lesson_planner_node import lesson_planner_node
from nodes.script_writter_node import script_writer_node
from nodes.story_board_node import storyboard_node
from nodes.code_generator_node import code_generator_node
from nodes.compiler_node import compiler_node
from nodes.code_validate_node import code_validate_node
from nodes.debug_node import debug_node
from nodes.clean_up_node import clean_up_node
from schema.state_schema import AgentState
from nodes.routers import route_after_validation, route_after_compilation

LESSON_PLANNER_NODE = "lesson_planner_node"
SCRIPT_WRITER_NODE = "script_writer_node"
STORYBOARD_NODE = "storyboard_node"
CODE_GENERATOR_NODE = "code_generator_node"
CODE_VALIDATE_NODE = "code_validate_node"
DEBUG_NODE = "debug_node"
COMPILER_NODE = "compiler_node"
CLEAN_UP_NODE = "clean_up_node"

def create_graph():
    graph = StateGraph(AgentState)
    graph.add_node(LESSON_PLANNER_NODE, lesson_planner_node)
    graph.add_node(SCRIPT_WRITER_NODE, script_writer_node)
    graph.add_node(STORYBOARD_NODE, storyboard_node)
    graph.add_node(CODE_GENERATOR_NODE, code_generator_node)
    graph.add_node(CODE_VALIDATE_NODE, code_validate_node)
    graph.add_node(DEBUG_NODE, debug_node)
    graph.add_node(COMPILER_NODE, compiler_node)
    graph.add_node(CLEAN_UP_NODE, clean_up_node)

    graph.add_edge(START, LESSON_PLANNER_NODE)
    graph.add_edge(LESSON_PLANNER_NODE, SCRIPT_WRITER_NODE)
    graph.add_edge(SCRIPT_WRITER_NODE, STORYBOARD_NODE)
    graph.add_edge(STORYBOARD_NODE, CODE_GENERATOR_NODE)
    graph.add_edge(CODE_GENERATOR_NODE, CODE_VALIDATE_NODE)
    
    graph.add_conditional_edges(
        CODE_VALIDATE_NODE, 
        route_after_validation,
        {
            "debug_node": DEBUG_NODE,
            "compiler_node": COMPILER_NODE,
            "clean_up_node": CLEAN_UP_NODE
        }
    )
    
    graph.add_edge(DEBUG_NODE, CODE_VALIDATE_NODE)
    
    graph.add_conditional_edges(
        COMPILER_NODE,
        route_after_compilation,
        {
            "debug_node": DEBUG_NODE,
            "clean_up_node": CLEAN_UP_NODE
        }
    )

    graph.add_edge(CLEAN_UP_NODE, END)

    app = graph.compile()
    return app
