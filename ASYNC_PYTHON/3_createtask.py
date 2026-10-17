"""create_task schedules a coroutine to run in the background and returns a Task."""
import asyncio

async def request(name:str)->str:
    print(name,": started")
    await asyncio.sleep(4)
    print(name,": finished")
    return name 

async def main():
    task1 = asyncio.create_task(request("A"))
    task2 = asyncio.create_task(request("B"))
    task3 = asyncio.create_task(request("C"))

    # Tasks start running once main() reaches an await.
    print("Tasks created:", task1, task2, task3)
    results = await asyncio.gather(task1, task2, task3)
    task4 = asyncio.create_task(request("D"))
    result_task4 = await task4
    print("Results:", results)
    print("Result of task4:", result_task4)

async def main2():
    # TaskGroup waits for all child tasks before leaving the block.
    async with asyncio.TaskGroup() as group:
        e= group.create_task(request("E"))
        f =group.create_task(request("F"))
        g= group.create_task(request("G"))

    print("All tasks in the TaskGroup have completed.")
    print("results: ", e.result(), f.result(), g.result())

if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(main2())