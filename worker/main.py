import sys
import uuid
from dotenv import load_dotenv
load_dotenv()

from nodes.graph import create_graph
from services.project_service import project_service
from schema.project_schema import Project
from schema.message_schema import MessagePayload

sys.stdout.reconfigure(encoding='utf-8')

from loguru import logger
logger.add("logs/app_{time}.log", rotation="500 MB", level="INFO", enqueue=True)

from services.redis_service import redis_service
import time
from config.settings import settings

def main():
    # Connect and initialize Redis consumer group
    if not redis_service.connect():
        logger.error("Could not connect to Redis. Stopping worker.")
        return
        
    redis_service.create_consumer_group(stream_name=settings.REDIS_STREAM_NAME, id="0", mkstream=True)
    
    logger.info("Starting Redis consumer loop...")
    while True:
        try:
            # Block for 5 seconds waiting for a message
            messages = redis_service.readstream(stream_name=settings.REDIS_STREAM_NAME, count=1, block=5000)
            
            if messages:
                for stream, message_list in messages:
                    for message_id, data in message_list:
                        logger.info(f"Received message ID {message_id}: {data}")
                        
                        try:
                            payload = MessagePayload(**data)
                        except Exception as e:
                            logger.error(f"Invalid message format: {e}")
                            continue

                        project_id = payload.id
                        prompt = payload.prompt
                        logger.info(f"Using prompt: {prompt}")

                        app = create_graph()

                        res = app.invoke(
                            {"prompt": prompt},
                            config={"configurable": {"thread_id": project_id}}
                        )
                        logger.info(f"Final output state: {res}")
                        
                        # Acknowledge the message
                        redis_service.ack_message(
                            stream_name=settings.REDIS_STREAM_NAME, 
                            message_id=message_id
                        )
                        
        except KeyboardInterrupt:
            logger.info("Shutting down consumer loop.")
            break
        except Exception as e:
            logger.error(f"Error in consumer loop: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
