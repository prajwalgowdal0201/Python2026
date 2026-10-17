# Python Learning

Notes and runnable examples while learning Python.

## Async Python (`ASYNC_PYTHON/`)

Requires Python 3.11+ (`asyncio.timeout` and `TaskGroup`).

| # | File | Topic |
|---|------|-------|
| - | [PYTHON_ASYNC_GUIDE.md](ASYNC_PYTHON/PYTHON_ASYNC_GUIDE.md) | Written guide: concepts, pitfalls, checklist |
| 1 | [1_SampleAsyncProgram.py](ASYNC_PYTHON/1_SampleAsyncProgram.py) | Coroutines, `await`, `asyncio.run` |
| 2 | [2_Sequential_vs_Concurrent.py](ASYNC_PYTHON/2_Sequential_vs_Concurrent.py) | Sequential vs `asyncio.gather` timing |
| 3 | [3_createtask.py](ASYNC_PYTHON/3_createtask.py) | `create_task` and `TaskGroup` |
| 4 | [4_asycn_timeout.py](ASYNC_PYTHON/4_asycn_timeout.py) | `asyncio.timeout` |
| 5 | [5_semaphoreAsync.py](ASYNC_PYTHON/5_semaphoreAsync.py) | Limiting concurrency with `Semaphore` |

## Run an example

```bash
python ASYNC_PYTHON/2_Sequential_vs_Concurrent.py
```
