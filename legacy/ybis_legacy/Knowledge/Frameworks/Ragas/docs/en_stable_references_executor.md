Executor - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.executor)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Executor

## Executor `dataclass`

```
Executor(desc: str = 'Evaluating', show_progress: bool = True, keep_progress_bar: bool = True, jobs: List[Any] = list(), raise_exceptions: bool = False, batch_size: Optional[int] = None, run_config: Optional[RunConfig] = None, pbar: Optional[tqdm] = None, _jobs_processed: int = 0, _cancel_event: Event = Event())
```

Executor class for running asynchronous jobs with progress tracking and error handling.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `desc` | `str` | Description for the progress bar |
| `show_progress` | `bool` | Whether to show the progress bar |
| `keep_progress_bar` | `bool` | Whether to keep the progress bar after completion |
| `jobs` | `List[Any]` | List of jobs to execute |
| `raise_exceptions` | `bool` | Whether to raise exceptions or log them |
| `batch_size` | `int` | Whether to batch (large) lists of tasks |
| `run_config` | `RunConfig` | Configuration for the run |
| `_nest_asyncio_applied` | `bool` | Whether nest\_asyncio has been applied |
| `_cancel_event` | `Event` | Event to signal cancellation |

### cancel

```
cancel() -> None
```

Cancel the execution of all jobs.

Source code in `src/ragas/executor.py`

|  |  |
| --- | --- |
| ``` 56 57 58 ``` | ``` def cancel(self) -> None:     """Cancel the execution of all jobs."""     self._cancel_event.set() ``` |

### is\_cancelled

```
is_cancelled() -> bool
```

Check if the execution has been cancelled.

Source code in `src/ragas/executor.py`

|  |  |
| --- | --- |
| ``` 60 61 62 ``` | ``` def is_cancelled(self) -> bool:     """Check if the execution has been cancelled."""     return self._cancel_event.is_set() ``` |

### submit

```
submit(callable: Callable, *args, name: Optional[str] = None, **kwargs) -> None
```

Submit a job to be executed, wrapping the callable with error handling and indexing to keep track of the job index.

Source code in `src/ragas/executor.py`

|  |  |
| --- | --- |
| ```  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 ``` | ``` def submit(     self,     callable: t.Callable,     *args,     name: t.Optional[str] = None,     **kwargs, ) -> None:     """     Submit a job to be executed, wrapping the callable with error handling and indexing to keep track of the job index.     """     # Use _jobs_processed for consistent indexing across multiple runs     callable_with_index = self.wrap_callable_with_index(         callable, self._jobs_processed     )     self.jobs.append((callable_with_index, args, kwargs, name))     self._jobs_processed += 1 ``` |

### clear\_jobs

```
clear_jobs() -> None
```

Clear all submitted jobs and reset counter.

Source code in `src/ragas/executor.py`

|  |  |
| --- | --- |
| ``` 105 106 107 108 ``` | ``` def clear_jobs(self) -> None:     """Clear all submitted jobs and reset counter."""     self.jobs.clear()     self._jobs_processed = 0 ``` |

### aresults `async`

```
aresults() -> List[Any]
```

Execute all submitted jobs and return their results asynchronously.
The results are returned in the order of job submission.

This is the async entry point for executing async jobs when already in an async context.

Source code in `src/ragas/executor.py`

|  |  |
| --- | --- |
| ``` 193 194 195 196 197 198 199 200 201 202 ``` | ``` async def aresults(self) -> t.List[t.Any]:     """     Execute all submitted jobs and return their results asynchronously.     The results are returned in the order of job submission.      This is the async entry point for executing async jobs when already in an async context.     """     results = await self._process_jobs()     sorted_results = sorted(results, key=lambda x: x[0])     return [r[1] for r in sorted_results] ``` |

### results

```
results() -> List[Any]
```

Execute all submitted jobs and return their results. The results are returned in the order of job submission.

This is the main sync entry point for executing async jobs.

Source code in `src/ragas/executor.py`

|  |  |
| --- | --- |
| ``` 204 205 206 207 208 209 210 211 212 213 214 215 ``` | ``` def results(self) -> t.List[t.Any]:     """     Execute all submitted jobs and return their results. The results are returned in the order of job submission.      This is the main sync entry point for executing async jobs.     """      async def _async_wrapper():         return await self.aresults()      apply_nest_asyncio()     return run(_async_wrapper) ``` |

## run\_async\_batch

```
run_async_batch(desc: str, func: Callable, kwargs_list: List[Dict], batch_size: Optional[int] = None)
```

Provide functionality to run the same async function with different arguments in parallel.

Source code in `src/ragas/executor.py`

|  |  |
| --- | --- |
| ``` 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 ``` | ``` def run_async_batch(     desc: str,     func: t.Callable,     kwargs_list: t.List[t.Dict],     batch_size: t.Optional[int] = None, ):     """     Provide functionality to run the same async function with different arguments in parallel.     """     run_config = RunConfig()     executor = Executor(         desc=desc,         keep_progress_bar=False,         raise_exceptions=True,         run_config=run_config,         batch_size=batch_size,     )      for kwargs in kwargs_list:         executor.submit(func, **kwargs)      return executor.results() ``` |

November 28, 2025




November 28, 2025

Back to top