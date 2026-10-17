#we use async when a program spends time waiting on many independant operations.
#like netwrok requests, web services , sickests, asynchronouse databases and file APIs
#while op is waiting the event lopp can let another operation make progress 
#its not multithreading its concurrency 
# if we have 3 netwioirk requests: sync  request1-> request -> request 3 
#async request 1 start -> request 2 start -> request 3 start -> request 1 finish -> request 2 finish -> request 3 finish

'''
couroutine function: a fucntion defined with keyword async is called couroutine 
await : suspends the current coroutine ultill the awaitable operation provide a result , and event loop can run other task while its suspended 
lets say i just called a async func withpout await: it just creates a couroutine object and python warns that that coroutine iobject was neevr awaited. 
'''

#simple async program 
import asyncio 

async def greet():
    print("Hwllo , How are you ?")
    await asyncio.sleep(3)
    print("I'm back after 3 seconds!")

#an asyncio.run i s required to run a async function 
async def main():
    await greet()

asyncio.run(main())

#so just calling a function i.e greet() doesnt execute it, it just creates a coroutine object 
#to actually run it, we need to use await inside another coroutine or use asyncio.run() at the top level
