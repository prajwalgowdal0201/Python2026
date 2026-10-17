# A Practical Guide to Python `async` and `await`

This guide explains what asynchronous Python is for, what `async` and `await` mean, when to use them, and how to avoid common mistakes. All examples are included here.

## The short version

Use `asyncio` when a program spends time waiting on many independent operations, especially network requests, web services, sockets, or asynchronous database and file APIs. While one operation is waiting, the event loop can let another operation make progress.

Async does not automatically make every program faster. It is usually not the right tool for CPU-heavy calculations, and it does not make blocking code non-blocking by itself.

## The key idea: waiting without stopping everything

Imagine a program making three web requests. A synchronous program can wait for request 1 to finish before it starts request 2. An asynchronous program can start the requests, then switch to another request whenever one is waiting for the network.

This is **concurrency**: multiple tasks make progress during overlapping periods. In typical `asyncio` code, those tasks run cooperatively on one thread; this is not the same as doing CPU calculations in parallel on multiple cores.

Async is most useful when there are many waits. If a program only does a little work, or must do each step after the previous one, ordinary synchronous code is often clearer.

## The vocabulary

- **Coroutine function:** a function declared with `async def`.
- **Coroutine object:** the value returned when a coroutine function is called. Creating it does not, by itself, run its body.
- **`await`:** suspends the current coroutine until another awaitable operation can provide a result. While it is suspended, the event loop can run other ready tasks.
- **Event loop:** the scheduler that runs coroutines and handles asynchronous I/O events.
- **Task:** a scheduled coroutine that the event loop can run independently while the caller does other work.
- **Awaitable:** an object that can be used with `await`, such as a coroutine or `asyncio.Task`.

## Your first async program

Save and run this as a Python file:

```python
import asyncio


async def greet():
    print("Hello")
    await asyncio.sleep(1)
    print("Goodbye")


asyncio.run(greet())
```

`asyncio.run()` runs the top-level coroutine and manages the event loop for a standalone script.

`await asyncio.sleep(1)` pauses this coroutine without blocking other async tasks. `time.sleep(1)` would block the event-loop thread.

## What happens if I leave out `await`?

Calling an async function only creates a coroutine object:

```python
async def greet():
    print("Hello")


greet()  # Creates a coroutine; its body does not run.
```

Python may warn that the coroutine was never awaited. To run it, either await it from another coroutine or pass it to `asyncio.run()` at the program's top level:

```python
async def main():
    await greet()


asyncio.run(main())
```

This is the issue in the original ending of `AsyncPyhton.py`: calling `main()` directly does not start the tasks inside it. Use `asyncio.run(main())` for a standalone script, or `await main()` when already inside an async function.

Leaving `await` off an ordinary, non-async function call is not a fix; regular functions run normally and can block. Also, an `async def` with no `await` is legal, but it runs its body without giving other tasks a chance to run until it returns.

## Sequential work versus concurrent work

This complete program compares sequential and concurrent simulated requests. Save it as a `.py` file and run it with Python:

```python
import asyncio
from time import perf_counter


async def request(name):
    print(name, "started")
    await asyncio.sleep(1)  # Simulate waiting for a response.
    print(name, "finished")
    return name


async def main():
    started = perf_counter()
    first = await request("A")
    second = await request("B")
    print("Sequential results:", first, second)
    print("Sequential seconds:", round(perf_counter() - started, 1))

    started = perf_counter()
    first, second = await asyncio.gather(request("A"), request("B"))
    print("Concurrent results:", first, second)
    print("Concurrent seconds:", round(perf_counter() - started, 1))


asyncio.run(main())
```

The first pair is sequential: each request waits for the other, taking about 2 seconds. `gather()` runs independent requests together, taking about 1 second. `asyncio.sleep()` simulates I/O waiting without needing a server.

## `asyncio.create_task`

Use `create_task()` to schedule work and continue before collecting its result. This snippet assumes `fetch_data()` is an async function:

```python
async def main():
    task = asyncio.create_task(fetch_data("report"))
    print("The request has been scheduled")
    result = await task
    print(result)
```

Keep a reference to important tasks and await or manage them. For related tasks in Python 3.11+, `TaskGroup` manages their lifetime as a group. This snippet assumes `fetch_data()` is defined:

```python
async def main():
    async with asyncio.TaskGroup() as group:
        first = group.create_task(fetch_data("first"))
        second = group.create_task(fetch_data("second"))

    print(first.result(), second.result())
```

The task group waits for its child tasks before leaving the block. If a child fails, the group cancels its unfinished siblings and reports the failure. Use `gather()` when collecting a simple set of results; use a task group when you want explicit structured ownership of related tasks.

## Is `asyncio.wait()` required?

No. `await` waits for an async result. `asyncio.wait()` is an optional helper for cases such as waiting for the first task to finish. Start with `await`, `gather()`, or `TaskGroup`.

For a simple timeout, Python 3.11+ provides `asyncio.timeout()`:

```python
async def main():
    try:
        async with asyncio.timeout(2):
            result = await fetch_data("slow operation")
    except TimeoutError:
        print("The operation took too long")
```

On older supported Python versions, `asyncio.wait_for(awaitable, timeout=2)` is a common alternative. A timeout or caller cancellation can cancel the awaited operation, so async operations should allow cancellation to propagate unless there is a specific reason to handle it.

## What if I do not use `async`?

Use normal `def` functions when the work is simple, synchronous, or CPU-heavy. There is no benefit in adding `async` if there is no asynchronous operation to await.

If you call a blocking function inside an async function, it still blocks the event-loop thread:

```python
async def bad_example():
    time.sleep(2)  # Blocks every asyncio task on this event loop.
```

For a blocking I/O function with no async version, `asyncio.to_thread()` moves it off the event-loop thread. This snippet assumes `read_large_file()` is a normal blocking function:

```python
async def main():
    result = await asyncio.to_thread(read_large_file, "data.txt")
    print(result)
```

`asyncio.to_thread()` is mainly useful for blocking I/O. For CPU-bound Python work, use a process pool or another approach that can use multiple CPU cores; async scheduling alone does not speed up the calculation.

## Limit how much work runs at once

Starting too many requests at once can overload a service. A semaphore caps how many operations run at once. This snippet assumes `fetch_data()` and `urls` are defined:

```python
async def fetch_limited(semaphore, url):
    async with semaphore:
        return await fetch_data(url)


async def main():
    semaphore = asyncio.Semaphore(10)
    results = await asyncio.gather(
        *(fetch_limited(semaphore, url) for url in urls)
    )
    print(results)
```

At most ten calls enter `fetch_data()` at once. Also respect the service's connection and request limits.

## Common mistakes

1. **Calling a coroutine without awaiting or scheduling it.** Use `await`, `asyncio.create_task()`, `asyncio.gather()`, or a task group.
2. **Using `time.sleep()` in async code.** Use `await asyncio.sleep()` when you need an async delay.
3. **Expecting CPU-heavy work to become faster.** Async helps overlap waits, not parallelize CPU calculations.
4. **Calling `asyncio.run()` from inside an active event loop.** In an async function, use `await` instead. Notebook environments often already run a loop.
5. **Making dependent work concurrent.** If step two needs step one's result, await step one first.
6. **Launching unbounded work.** Use a semaphore, bounded queue, or a client library's connection limit.
7. **Forgetting errors and cancellation.** Await tasks and decide how your application should report failures and respond when work is cancelled.

## A practical decision checklist

- Is most of the time spent waiting on I/O? Async may be a good fit.
- Does the library you use provide an async API? Prefer it over wrapping synchronous calls in an async function.
- Are operations independent? They may be run concurrently.
- Is the work CPU-heavy or very small? Prefer ordinary synchronous code, or use an appropriate process-based solution for CPU work.
- Can the number of simultaneous operations grow large? Add a concurrency limit.
- Does every coroutine have an owner that awaits it or manages it as a task? If not, fix that before shipping.

## A useful mental model

Think of `await` as: “Pause this coroutine while the event loop runs other work.” It does **not** mean “run this on another thread.” Replace `asyncio.sleep()` in the comparison program with an async library call to use this pattern in a real application.