import asyncio

#limit how many concurrent tasks can run at once 
#to prevent the service overload , a semaphore caps hopw many operations run at once 
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