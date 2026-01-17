import redis
import time
from functools import wraps

# Step 1: Initialize Redis connection as a singleton class
class RedisConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisConnection, cls).__new__(cls)
            cls._instance.connection = redis.Redis(*args, **kwargs)
        return cls._instance

# Step 2: Implement exponential backoff logic in `exponential_backoff.py`
def exponential_backoff(retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except redis.ConnectionError as e:
                    attempt += 1
                    store_attempt(func.__name__, attempt)
                    if attempt == retries:
                        raise e
                    time.sleep(delay * (2 ** (attempt - 1)))
        return wrapper
    return decorator

# Step 3: Store attempt counts and timestamps in Redis using `store_attempt()` function
def store_attempt(endpoint, attempt):
    redis_conn = RedisConnection().connection
    key = f"retry:{endpoint}"
    redis_conn.hincrby(key, 'count', amount=1)
    redis_conn.hset(key, 'last_attempt', time.time())

# Step 4: Retrieve attempt counts from Redis using `get_attempt_count()` function
def get_attempt_count(endpoint):
    redis_conn = RedisConnection().connection
    key = f"retry:{endpoint}"
    count = redis_conn.hget(key, 'count')
    return int(count) if count else 0

# Step 5: Update API signatures to include retryable endpoints
@exponential_backoff(retries=5, delay=2)
def example_api_call():
    # Example function that might need retries
    pass