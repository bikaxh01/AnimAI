import sys
from langgraph.graph import StateGraph,START,END
from nodes.lesson_planner_node import lesson_planner_node
from nodes.script_writter_node import script_writer_node
from nodes.story_board_node import storyboard_node
from nodes.code_generator_node import code_generator_node
from nodes.compiler_node import compiler_node
from schema.state_schema import AgentState

sys.stdout.reconfigure(encoding='utf-8')

def main ():

  
  LESSON_PLANNER_NODE = "lesson_planner_node"
  SCRIPT_WRITER_NODE = "script_writer_node"
  STORYBOARD_NODE = "storyboard_node"
  CODE_GENERATOR_NODE = "code_generator_node"
  COMPILER_NODE = "compiler_node"
  
  graph = StateGraph(AgentState)
  graph.add_node(LESSON_PLANNER_NODE, lesson_planner_node)
  graph.add_node(SCRIPT_WRITER_NODE, script_writer_node)
  graph.add_node(STORYBOARD_NODE, storyboard_node)
  graph.add_node(CODE_GENERATOR_NODE, code_generator_node)
  graph.add_node(COMPILER_NODE, compiler_node)

  graph.add_edge(START, LESSON_PLANNER_NODE)
  graph.add_edge(LESSON_PLANNER_NODE, SCRIPT_WRITER_NODE)
  graph.add_edge(SCRIPT_WRITER_NODE, STORYBOARD_NODE)
  graph.add_edge(STORYBOARD_NODE, CODE_GENERATOR_NODE)
  graph.add_edge(CODE_GENERATOR_NODE, COMPILER_NODE)
  graph.add_edge(COMPILER_NODE, END)

  app = graph.compile()
  
  res = app.invoke({"prompt": "Make video on binary search vs linear search in go lang"})
  print("Final output state:", res)

 

if __name__ == "__main__":

    main()
