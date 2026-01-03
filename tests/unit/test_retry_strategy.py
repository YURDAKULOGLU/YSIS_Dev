import unittest
from src.agentic.core.strategies.retry_strategy import RetryStrategy
import time

class TestRetryStrategy(unittest.TestCase):
    def setUp(self):
        # Use short cooldown_period (0.5s) for fast tests - default is 60s!
        self.retry_strategy = RetryStrategy(base_delay=0.1, max_retries=3, jitter_range=0.05, cooldown_period=0.5)

    def test_exponential_backoff(self):
        attempt = 0
        delays = []
        while attempt < self.retry_strategy.max_retries:
            delay = self.retry_strategy.get_delay(attempt)
            delays.append(delay)
            time.sleep(delay)
            attempt += 1

        expected_delays = [self.retry_strategy.base_delay, self.retry_strategy.base_delay * 2, self.retry_strategy.base_delay * 4]
        for i in range(len(delays)):
            self.assertAlmostEqual(delays[i], expected_delays[i], delta=self.retry_strategy.jitter_range * self.retry_strategy.base_delay)

    def test_circuit_breaker(self):
        self.retry_strategy.record_failure()
        self.retry_strategy.record_failure()
        self.retry_strategy.record_failure()

        self.assertFalse(self.retry_strategy.should_retry())

        time.sleep(self.retry_strategy.cooldown_period + 0.1)
        self.assertTrue(self.retry_strategy.should_retry())

    def test_reset(self):
        self.retry_strategy.record_failure()
        self.retry_strategy.reset()

        self.assertEqual(self.retry_strategy.consecutive_failures, 0)

    def test_execute_with_retries_success(self):
        def success_func():
            return "success"

        result = self.retry_strategy.execute_with_retries(success_func)
        self.assertEqual(result, "success")

    def test_execute_with_retries_failure(self):
        def failure_func():
            raise Exception("failure")

        with self.assertRaises(Exception) as context:
            self.retry_strategy.execute_with_retries(failure_func)

        self.assertTrue("failure" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
