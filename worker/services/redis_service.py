import redis
from loguru import logger
from config.settings import settings
import random

class RedisService:
    def __init__(self):
        self.client = None
        self.consumer_name = f"{settings.REDIS_GROUP_NAME}_{random.randint(1000, 9999)}"

    def connect(self) -> bool:
        try:
            kwargs = {
                "host": settings.REDIS_HOST,
                "port": settings.REDIS_PORT,
                "decode_responses": True
            }
            if settings.REDIS_PASSWORD:
                kwargs["password"] = settings.REDIS_PASSWORD
                
            self.client = redis.Redis(**kwargs)
            # Ping to check connection
            self.client.ping()
            logger.info("Connected to Redis successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None
            return False

    def close(self):
        if self.client:
            self.client.close()
            logger.info("Redis connection closed.")
            self.client = None

    def writestream(self, stream_name: str, data: dict):
        if not self.client:
            logger.warning("Redis client is not connected.")
            return None
        try:
            # xadd writes to the stream. data must be a dictionary.
            result = self.client.xadd(stream_name, data)
            logger.debug(f"Wrote to stream {stream_name}: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to write to stream {stream_name}: {e}")
            return None

    def readstream(self, stream_name: str, count: int = 1, block: int = 0, last_id: str = ">"):
        if not self.client:
            logger.warning("Redis client is not connected.")
            return None
        try:
            # xreadgroup reads from a consumer group.
            # last_id=">" reads only new messages. 
            # block=0 means block indefinitely. block can be in ms.
            result = self.client.xreadgroup(
                groupname=settings.REDIS_GROUP_NAME,
                consumername=self.consumer_name,
                streams={stream_name: last_id},
                count=count,
                block=block
            )
            return result
        except Exception as e:
            logger.error(f"Failed to read from stream {stream_name} with group {settings.REDIS_GROUP_NAME}: {e}")
            return None

    def create_consumer_group(self, stream_name: str, id: str = "0", mkstream: bool = True):
        if not self.client:
            logger.warning("Redis client is not connected.")
            return False
        try:
            self.client.xgroup_create(
                name=stream_name,
                groupname=settings.REDIS_GROUP_NAME,
                id=id,
                mkstream=mkstream
            )
            logger.info(f"Consumer group '{settings.REDIS_GROUP_NAME}' created for stream '{stream_name}'.")
            return True
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP Consumer Group name already exists" in str(e):
                logger.info(f"Consumer group '{settings.REDIS_GROUP_NAME}' already exists for stream '{stream_name}'.")
                return True
            else:
                logger.error(f"Failed to create consumer group '{settings.REDIS_GROUP_NAME}': {e}")
                return False
        except Exception as e:
            logger.error(f"Failed to create consumer group '{settings.REDIS_GROUP_NAME}': {e}")
            return False

    def ack_message(self, stream_name: str, message_id: str):
        if not self.client:
            logger.warning("Redis client is not connected.")
            return False
        try:
            result = self.client.xack(stream_name, settings.REDIS_GROUP_NAME, message_id)
            logger.debug(f"Acknowledged message {message_id} in stream {stream_name}")
            return result
        except Exception as e:
            logger.error(f"Failed to acknowledge message {message_id}: {e}")
            return False

redis_service = RedisService()
