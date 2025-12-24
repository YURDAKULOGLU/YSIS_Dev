
import redis


class RedisQueue:
    """
    A simple Redis-based queue implementation for message passing between agents.
    """

    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)

    def publish(self, channel: str, message: str) -> None:
        """
        Publish a message to the specified Redis channel.

        Args:
            channel (str): The name of the channel to publish to.
            message (str): The message to send.
        """
        self.redis_client.publish(channel, message)

    def subscribe(self, channels: list[str]) -> redis.client.PubSub:
        """
        Subscribe to one or more Redis channels.

        Args:
            channels (list[str]): A list of channel names to subscribe to.

        Returns:
            redis.client.PubSub: The PubSub object for listening to messages.
        """
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(*channels)
        return pubsub
