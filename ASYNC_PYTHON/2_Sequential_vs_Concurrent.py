import asyncio
from time import perf_counter

#asyncio.gather is used to run multiple asynchronous tasks concurrently and wait for all of them to complete.
#while asyncio.run is used to run the main asynchronous function and manage the event loop.

async def request(name:str)->str:
    print(name,": started")
    await asyncio.sleep(2)
    print(name,": finished")
    return name

async def main():
    started = perf_counter()
    first = await request("A")
    second = await request("B")
    print("Sequentila results: ",first,second)
    print("Time taken: ",round(perf_counter()-started,1))

    started = perf_counter()
    first , second = await asyncio.gather(request("A"),request("B"))
    print("Concurrent results: ",first,second)
    print("time taken: ",round(perf_counter()-started,1))

if __name__ == "__main__":
    asyncio.run(main())