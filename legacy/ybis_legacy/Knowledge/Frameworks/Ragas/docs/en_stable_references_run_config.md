RunConfig - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.run_config)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# RunConfig

## RunConfig `dataclass`

```
RunConfig(timeout: int = 180, max_retries: int = 10, max_wait: int = 60, max_workers: int = 16, exception_types: Union[Type[BaseException], Tuple[Type[BaseException], ...]] = (Exception,), log_tenacity: bool = False, seed: int = 42)
```

Configuration for a timeouts, retries and seed for Ragas operations.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `timeout` | `int` | Maximum time (in seconds) to wait for a single operation, by default 180. | `180` |
| `max_retries` | `int` | Maximum number of retry attempts, by default 10. | `10` |
| `max_wait` | `int` | Maximum wait time (in seconds) between retries, by default 60. | `60` |
| `max_workers` | `int` | Maximum number of concurrent workers, by default 16. | `16` |
| `exception_types` | `Union[Type[BaseException], Tuple[Type[BaseException], ...]]` | Exception types to catch and retry on, by default (Exception,). | `(Exception,)` |
| `log_tenacity` | `bool` | Whether to log retry attempts using tenacity, by default False. | `False` |
| `seed` | `int` | Random seed for reproducibility, by default 42. | `42` |

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `rng` | `Generator` | Random number generator initialized with the specified seed. |

Notes

The `__post_init__` method initializes the `rng` attribute as a numpy random
number generator using the specified seed.

## add\_retry

```
add_retry(fn: WrappedFn, run_config: RunConfig) -> WrappedFn
```

Adds retry functionality to a given function using the provided RunConfig.

This function wraps the input function with retry logic using the tenacity library.
It configures the retry behavior based on the settings in the RunConfig.

Notes

* If log\_tenacity is enabled in the RunConfig, it sets up logging for retry attempts.
* The retry logic uses exponential backoff with random jitter for wait times.
* The number of retry attempts and exception types to retry on are configured
  based on the RunConfig.

Source code in `src/ragas/run_config.py`

|  |  |
| --- | --- |
| ``` 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 ``` | ``` def add_retry(fn: WrappedFn, run_config: RunConfig) -> WrappedFn:     """     Adds retry functionality to a given function using the provided RunConfig.      This function wraps the input function with retry logic using the tenacity library.     It configures the retry behavior based on the settings in the RunConfig.      Notes     -----     - If log_tenacity is enabled in the RunConfig, it sets up logging for retry attempts.     - The retry logic uses exponential backoff with random jitter for wait times.     - The number of retry attempts and exception types to retry on are configured       based on the RunConfig.     """     # configure tenacity's after section wtih logger     if run_config.log_tenacity is not None:         logger = logging.getLogger(f"ragas.retry.{fn.__name__}")         tenacity_logger = after_log(logger, logging.DEBUG)     else:         tenacity_logger = after_nothing      r = Retrying(         wait=wait_random_exponential(multiplier=1, max=run_config.max_wait),         stop=stop_after_attempt(run_config.max_retries),         retry=retry_if_exception_type(run_config.exception_types),         reraise=True,         after=tenacity_logger,     )     return r.wraps(fn) ``` |

## add\_async\_retry

```
add_async_retry(fn: WrappedFn, run_config: RunConfig) -> WrappedFn
```

Decorator for retrying a function if it fails.

Source code in `src/ragas/run_config.py`

|  |  |
| --- | --- |
| ```  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 ``` | ``` def add_async_retry(fn: WrappedFn, run_config: RunConfig) -> WrappedFn:     """     Decorator for retrying a function if it fails.     """     # configure tenacity's after section wtih logger     if run_config.log_tenacity is not None:         logger = logging.getLogger(f"TENACITYRetry[{fn.__name__}]")         tenacity_logger = after_log(logger, logging.DEBUG)     else:         tenacity_logger = after_nothing      r = AsyncRetrying(         wait=wait_random_exponential(multiplier=1, max=run_config.max_wait),         stop=stop_after_attempt(run_config.max_retries),         retry=retry_if_exception_type(run_config.exception_types),         reraise=True,         after=tenacity_logger,     )     return r.wraps(fn) ``` |

November 28, 2025




November 28, 2025

Back to top