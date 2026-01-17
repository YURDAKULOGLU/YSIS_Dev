from typing import Callable, Optional
import time
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetryStrategy:
    def __init__(self, base_delay: float = 1.0, max_retries: int = 5, jitter_range: float = 0.2, cooldown_period: float = 60):
        self.base_delay = base_delay
        self.max_retries = max_retries
        self.jitter_range = jitter_range
        self.cooldown_period = cooldown_period
        self.consecutive_failures = 0
        self.last_failure_time = 0.0

    def should_retry(self) -> bool:
        if time.time() - self.last_failure_time < self.cooldown_period and self.consecutive_failures >= self.max_retries:
            return False
        return True

    def get_delay(self, attempt: int) -> float:
        jitter = random.uniform(-self.jitter_range * self.base_delay, self.jitter_range * self.base_delay)
        delay = self.base_delay * (2 ** attempt) + jitter
        return max(0, delay)

    def record_failure(self):
        self.consecutive_failures += 1
        self.last_failure_time = time.time()
        logger.info(f"Recorded failure. Consecutive failures: {self.consecutive_failures}")

    def reset(self):
        self.consecutive_failures = 0
        logger.info("Reset retry strategy.")

    def execute_with_retries(self, func: Callable, *args, **kwargs) -> Optional[object]:
        attempt = 0
        last_error: Exception | None = None
        while attempt < self.max_retries:
            try:
                result = func(*args, **kwargs)
                self.reset()
                return result
            except Exception as e:
                last_error = e
                if not self.should_retry():
                    logger.error(f"Max retries reached. Last exception: {e}")
                    raise
                delay = self.get_delay(attempt)
                logger.info(f"Attempt {attempt + 1} failed, retrying in {delay:.2f} seconds...")
                time.sleep(delay)
                attempt += 1
                self.record_failure()
        logger.error("All retries exhausted.")
        if last_error:
            raise last_error
        raise RuntimeError("All retries exhausted with no captured exception.")
