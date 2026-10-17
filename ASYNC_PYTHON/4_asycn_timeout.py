"""asyncio.timeout cancels the awaited operation and raises TimeoutError."""
import asyncio

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