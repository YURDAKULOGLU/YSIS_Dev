import time
import random

def retry_with_exponential_backoff(func, args=(), kwargs=None, retries=5, backoff_in_seconds=1, max_jitter=0.5):
    """
    Retries a function with an exponential backoff strategy.

    This function will attempt to call the provided function up to `retries` times,
    with an exponentially increasing delay between attempts. The delay starts at
    `backoff_in_seconds` and doubles with each retry, plus some random jitter up to
    `max_jitter` seconds to avoid synchronization issues.

    :param func: The function to be retried.
    :param args: Positional arguments for the function.
    :param kwargs: Keyword arguments for the function.
    :param retries: Number of times to retry before giving up.
    :param backoff_in_seconds: Initial delay between retries in seconds.
    :param max_jitter: Maximum random jitter added to the delay in seconds.

    :return: The result of the function if successful within retries, otherwise None.
    """
    kwargs = kwargs or {}
    attempt = 0
    while attempt < retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                delay = backoff_in_seconds * (2 ** attempt) + random.uniform(0, max_jitter)
                time.sleep(delay)
                attempt += 1
            else:
                print("Max retries reached. Giving up.")
                return None

# Example usage:
def sample_function():
    # Simulate a function that might fail
    if random.choice([True, False]):
        raise ValueError("Simulated error")
    return "Success"

result = retry_with_exponential_backoff(sample_function)
print(result)