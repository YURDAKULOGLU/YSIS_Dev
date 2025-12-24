
## Redis Integration

Redis is used as a message queue for multi-agent communication in the YBIS_Dev environment. The `RedisQueue` class in `src/agentic/infrastructure/redis_queue.py` provides methods to publish and subscribe to messages.

### Key Features:
- **Publish**: Send messages to specified channels.
- **Subscribe**: Listen to one or more channels for incoming messages.
