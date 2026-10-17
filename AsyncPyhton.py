#async keytword is used to deinfe a asynchronous function. 
#such functions can pause while waiting for a task to complete , allowing other tasks to run wihtout blocking the program 
import asyncio

async def greet():
    print("Hello, world!")
    await asyncio.sleep(2)
    print("Goodbye, world!")

asyncio.run(greet())
#
#running multiple taks simultaneously .

#with help of async multiple tasks can run wiohtout waiting for other task to ocmplete 
async def task1():
    print("Task 1 started")
    await asyncio.sleep(3)
    print("task 1 completed")

async def task2():
    print("task 2 also started")
    await asyncio.sleep(1)
    print("task 2 completed")\

async def main():
    await asyncio.gather(task1(),task2())
    print("All tasks completed")

asyncio.run(main())