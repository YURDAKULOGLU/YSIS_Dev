import time
import logging

class RetryPolicy:
    def __init__(self, max_retries=5, initial_delay=1, backoff_factor=2, max_delay=60):
        """
        Initializes the RetryPolicy with specified parameters.
        
        :param max_retries: Maximum number of retry attempts.
        :param initial_delay: Initial delay between retries in seconds.
        :param backoff_factor: Factor by which the delay should increase after each retry.
        :param max_delay: Maximum delay between retries in seconds.
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay

    def execute_with_retry(self, func, *args, **kwargs):
        """
        Executes a function with retry logic using exponential backoff.
        
        :param func: The function to be executed.
        :param args: Positional arguments for the function.
        :param kwargs: Keyword arguments for the function.
        :return: Result of the function if successful within retries.
        :raises Exception: If all retries fail, raises the last exception encountered.
        """
        delay = self.initial_delay
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed with error: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(delay)
                    delay = min(delay * self.backoff_factor, self.max_delay)
                else:
                    raise