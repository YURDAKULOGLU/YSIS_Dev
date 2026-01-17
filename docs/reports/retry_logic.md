docs/RETRY_LOGIC.md

# Exponential Backoff Mechanism Implementation

In this project, we implement an exponential backoff mechanism to handle retries in a more efficient manner. The exponential backoff algorithm increases the wait time between attempts exponentially with each retry, up to a maximum number of attempts or until the operation succeeds.

## How It Works
1. **Initial Delay**: Start with a base delay.
2. **Exponential Increase**: Each subsequent retry waits for an increasingly longer period.
3. **Jitter (Optional)**: To avoid synchronization issues, a small random value can be added to the delay.
4. **Maximum Retries**: Limit the number of retries to prevent infinite loops.

## Formula
The delay for the nth attempt is calculated using the formula:
\[ \text{delay} = \text{base\_delay} \times 2^n + \text{jitter} \]

Where:
- `base_delay` is the initial wait time.
- `n` is the number of attempts made so far (starting from 0).
- `jitter` is an optional random value to add variability.

## Example
For a base delay of 1 second and 3 retries, the delays would be:
- First retry: \( 1 \times 2^0 = 1 \) second
- Second retry: \( 1 \times 2^1 = 2 \) seconds
- Third retry: \( 1 \times 2^2 = 4 \) seconds

exponential_backoff.py

```python
import time
import random

def exponential_backoff(base_delay, max_retries, action):
    """
    Perform an action with exponential backoff retries.

    :param base_delay: The initial delay between attempts in seconds.
    :param max_retries: The maximum number of retry attempts.
    :param action: A callable representing the action to perform.
    """
    for attempt in range(max_retries):
        try:
            return action()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < max_retries - 1:
                # Calculate delay using exponential backoff
                delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                raise Exception("All retry attempts failed")
```