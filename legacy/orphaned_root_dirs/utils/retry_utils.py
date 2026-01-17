import time
import random

def exponential_backoff_retry(func, args=(), kwargs={}, max_retries=5, initial_delay=1, backoff_factor=2, jitter=0):
    """
    Retry a function with an exponential backoff mechanism.

    This function will attempt to execute `func` up to `max_retries` times. 
    If `func` raises an exception, it will wait for a delay that increases 
    exponentially based on the `backoff_factor` and optionally add some random 
    jitter to avoid thundering herd problems. The delay before each retry is calculated as:
    
        delay = initial_delay * (backoff_factor ** attempt) + random.uniform(-jitter, jitter)
    
    Parameters:
    - func: The function to retry.
    - args: Positional arguments to pass to the function.
    - kwargs: Keyword arguments to pass to the function.
    - max_retries: Maximum number of retries.
    - initial_delay: Initial delay between retries in seconds.
    - backoff_factor: Factor by which the delay should increase each time.
    - jitter: Random delay factor to add or subtract from the calculated delay.

    Returns:
    - The result of the function if successful within the max_retries.
    
    Raises:
    - Exception: If the function fails after max_retries attempts.
    """
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            delay = initial_delay * (backoff_factor ** attempt) + random.uniform(-jitter, jitter)
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise