import sys
import uuid
from dotenv import load_dotenv
load_dotenv()

from nodes.graph import create_graph
from services.project_service import project_service
from schema.project_schema import Project

sys.stdout.reconfigure(encoding='utf-8')

from loguru import logger
logger.add("logs/app_{time}.log", rotation="500 MB", level="INFO", enqueue=True)

def main ():
  project_id = "7c1c700a-f5f3-45af-a52b-f4e02b754fa4"
  
  # Fetch the project from the API
  project_data = project_service.get_by_id(project_id)
  
  if not project_data:
      logger.error(f"Failed to fetch project for id: {project_id}")
      return
      
  try:
      project = Project(**project_data)
  except Exception as e:
      logger.error(f"Failed to parse project data: {e}")
      return

  prompt = project.prompt
  logger.info(f"Using prompt: {prompt}")

  app = create_graph()

  res = app.invoke(
      {"prompt": prompt},
      config={"configurable": {"thread_id": project_id}}
  )
  logger.info(f"Final output state: {res}")
  # mermaid_code = app.get_graph().draw_mermaid()
  # print(mermaid_code)
 



if __name__ == "__main__":

    main()
    # single_node_test()
