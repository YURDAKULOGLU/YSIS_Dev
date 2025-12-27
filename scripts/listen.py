
import asyncio
import os
import json
import logging
from datetime import datetime
import redis.asyncio as redis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [REDIS-LISTENER] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CHANNELS = ["ybis-events", "tasks", "system"]

async def process_message(channel: str, message: str):
    """Process incoming messages from Redis."""
    try:
        # Try to parse JSON
        data = json.loads(message)
        logger.info(f"Received on {channel}: {json.dumps(data, indent=2)}")
        
        # TODO: Add logic here to react to events
        # e.g., if channel == 'tasks' and data['status'] == 'NEW', trigger something.

    except json.JSONDecodeError:
        logger.warning(f"Received raw text on {channel}: {message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

async def listen():
    """Main listener loop."""
    logger.info(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}...")
    
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        await r.ping()
        logger.info("Connected to Redis successfully.")

        pubsub = r.pubsub()
        await pubsub.subscribe(*CHANNELS)
        logger.info(f"Subscribed to channels: {CHANNELS}")

        async for message in pubsub.listen():
            if message["type"] == "message":
                await process_message(message["channel"], message["data"])

    except ConnectionError:
        logger.error("Could not connect to Redis. Is it running?")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Check if running in event loop compatible environment
        asyncio.run(listen())
    except KeyboardInterrupt:
        logger.info("Shutting down listener...")
