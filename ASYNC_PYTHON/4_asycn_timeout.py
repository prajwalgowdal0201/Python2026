import asyncio
#we can timeout async io operations also but should catch the execptions 

async def request():
    print("Request started")
    await asyncio.sleep(5)
    print("Request finished")

async def main():
    try:
        async with asyncio.timeout(6):
            await request()
    except asyncio.TimeoutError:
        print("Request timed out")
    else:
        print("Request completed successfully")

if __name__ == "__main__":
    asyncio.run(main())