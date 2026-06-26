import sys
import uuid
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph,START,END
from nodes.lesson_planner_node import lesson_planner_node
from nodes.script_writter_node import script_writer_node
from nodes.story_board_node import storyboard_node
from nodes.code_generator_node import code_generator_node
from nodes.compiler_node import compiler_node
from nodes.code_validate_node import code_validate_node
from nodes.debug_node import debug_node
from nodes.clean_up_node import clean_up_node
from schema.state_schema import AgentState

sys.stdout.reconfigure(encoding='utf-8')

from loguru import logger
logger.add("logs/app_{time}.log", rotation="500 MB", level="INFO", enqueue=True)

LESSON_PLANNER_NODE = "lesson_planner_node"
SCRIPT_WRITER_NODE = "script_writer_node"
STORYBOARD_NODE = "storyboard_node"
CODE_GENERATOR_NODE = "code_generator_node"
CODE_VALIDATE_NODE = "code_validate_node"
DEBUG_NODE = "debug_node"
COMPILER_NODE = "compiler_node"
CLEAN_UP_NODE = "clean_up_node"

def route_after_validation(state: AgentState) -> str:
    if state.has_error:
        if getattr(state, "debug_attempts", 0) >= 5:
            logger.error("Max debug attempts reached. Ending graph.")
            return CLEAN_UP_NODE
        return DEBUG_NODE
    return COMPILER_NODE

def route_after_compilation(state: AgentState) -> str:
    if state.has_error:
        if getattr(state, "debug_attempts", 0) >= 5:
            logger.error("Max debug attempts reached during compilation. Ending graph.")
            return CLEAN_UP_NODE
        return DEBUG_NODE
    return CLEAN_UP_NODE

def main ():
  
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
  res = app.invoke({"prompt": "Explain the list in pythoon in short around 4-5 sec video only only 2 topic what is list . and how to append list"},config={"configurable": {"thread_id": str(uuid.uuid4())}})
  logger.info(f"Final output state: {res}")
  # mermaid_code = app.get_graph().draw_mermaid()
  # print(mermaid_code)
 



if __name__ == "__main__":

    main()
    # single_node_test()
