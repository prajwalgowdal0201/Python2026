"""A Semaphore caps how many operations run at once to avoid overloading a service."""
import asyncio

async def request():
    print("Request started")
    await asyncio.sleep(2)
    print("Request finished")

async def main():
    semaphore = asyncio.Semaphore(3)  # Limit to 3 concurrent requests

    async def sem_request():
        async with semaphore:
            await request()

    tasks = [sem_request() for _ in range(10)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())