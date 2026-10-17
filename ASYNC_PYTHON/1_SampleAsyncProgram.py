# Use async when a program spends time waiting on many independent operations,
# such as network requests, web services, sockets, async databases, and file APIs.
# While one operation waits, the event loop lets another make progress. 
# This is concurrency, not multithreading. 
# Sync:  request 1 -> request 2 -> request 3 (one after another) 
# Async: start 1 -> start 2 -> start 3 -> finish 1 -> finish 2 -> finish 3

'''
coroutine function: a function defined with `async def`. 
await: suspends the current coroutine until the awaitable has a result; the event loop can run other tasks meanwhile. 
Calling a coroutine function without await only creates a coroutine object; Python warns it was never awaited. 
'''

# Simple async program 
import asyncio 

async def greet():
    print("Hello, how are you?")
    await asyncio.sleep(3)
    print("I'm back after 3 seconds!")

# asyncio.run starts the event loop and runs the top-level coroutine. 
async def main():
    await greet()

asyncio.run(main())

# Calling greet() alone only creates a coroutine object. 
# To run it, await it inside another coroutine or pass it to asyncio.run() at the top level.
