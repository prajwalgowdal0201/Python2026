#asyncio.create_task 
#use create task to just start a task and continue , not wait for its result and collect it later. 
#it just schedules the task to run in the background and returns immediately.
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

    #creatye task creates a coiroutine object and executes it but does not wait for its result immediately
    # At this point, all tasks are running concurrently in the background.
    #to get the results of these tasks, we need to await them or use asyncio.gather as shown below.

    print("Tasks created:", task1, task2, task3)
    # Wait for all tasks to complete and collect their results
    results = await asyncio.gather(task1, task2, task3)
    task4 = asyncio.create_task(request("D"))
    result_task4 = await task4
    print("Results:", results)
    print("Result of task4:", result_task4)

async def main2():
    #using TaskGroup 
    #taskgroup allows us to manage multiple tasks together and ensures that all tasks are completed before exiting
    # the group.
    async with asyncio.TaskGroup() as group:
        e= group.create_task(request("E"))
        f =group.create_task(request("F"))
        g= group.create_task(request("G"))

    print("All tasks in the TaskGroup have completed.")
    print("results: ", e.result(), f.result(), g.result())

if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(main2())