
import redis
import sys

def publish_test():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.publish('ybis-events', '{"event": "TEST_EVENT", "source": "manual_test"}')
    print("Test message published.")

if __name__ == "__main__":
    publish_test()
