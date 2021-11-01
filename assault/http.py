import asyncio
import os
import time
import requests

def fetch(url):
    """Make a request and return the results"""
    started_at = time.monotonic()
    response = requests.get(url)
    request_time = time.monotonic() - started_at
    return {"status_code": response.status_code, "request_time": request_time}



async def worker(name, queue, results):
    """A function to take unmake requests from a queue and perform a work;
    then add restuls to the results list
     """


    # it listens forever
    loop = asyncio.get_event_loop()
    while True:
        # take event from queue
        url = await queue.get()
        if os.getenv("DEBUG"):
            print(f"{name} - Fethcing {url}")
        # schedule execution of fetch with url
        future_result = loop.run_in_executor(None, fetch, url)
        # wait until finished
        result = await future_result
        # append result
        results.append(result)
        # mark task as done
        queue.task_done()
        # infinite loop => start again



async def distribute_work(url, requests, concurrency, results):
    """Divide the work into batches and collect the final results"""
    queue = asyncio.Queue()
    # put requests in a queue
    for _ in range(requests):
        queue.put_nowait(url)

    # create as many thread as desired
    tasks = []
    for i in range(concurrency):
        task = asyncio.create_task(worker(f"worker-{i+1}", queue, results))
        tasks.append(task)

    # calculate time
    started_at = time.monotonic()
    # wait until queue is empty
    await queue.join()
    total_time = time.monotonic() - started_at

    # close workers otherwise thread will live forever
    for task in tasks:
        task.cancel()

    # print('-----')
    # print(
    #     f"{concurrency} workers took {total_time} seconds to complete {len(results)} results"
    # )
    # print('------------')
    # print(results)

    return total_time



def assault(url, requests, concurrency):
    """The entry point to making requests"""
    results = []
    total_time = asyncio.run(distribute_work(url, requests, concurrency, results))
    return total_time, results