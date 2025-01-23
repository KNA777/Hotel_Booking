from src.config import settings
from src.connectors.redis_connect import RedisManager


redis_manager = RedisManager(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
