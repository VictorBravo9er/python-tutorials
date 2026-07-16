# %% [markdown]
# # Tutorial 12: Advanced Asyncio & Structured Concurrency
#
# Asynchronous programming allows writing high-performance, single-threaded concurrent applications. Beyond basic `async/await` and `asyncio.gather`, production-grade systems rely on structured concurrency and worker-queue distribution.
#
# In this notebook, we look at:
# 1. Structured Concurrency with `asyncio.TaskGroup` (Python 3.11+)
# 2. Worker Queue Distribution with `asyncio.Queue` (Producer-Consumer pattern)
# 3. Asynchronous Synchronization with `asyncio.Event` and `asyncio.Lock`

# %%
import asyncio
import time

# %% [markdown]
# ## 1. Structured Concurrency with TaskGroup
# Prior to Python 3.11, running multiple tasks concurrently was done using `asyncio.gather`. However, `gather` has poor error handling: if one task fails, others continue running in the background, creating leaked tasks.
#
# `asyncio.TaskGroup` provides **structured concurrency**: if any task inside the group fails, all other active tasks in the group are automatically cancelled, and an `ExceptionGroup` is raised.

# %%
async def task_success(name, delay):
    print(f"[Task {name}] Starting (will sleep {delay}s)...")
    await asyncio.sleep(delay)
    print(f"[Task {name}] Done!")
    return f"{name}_result"

async def task_failure(name, delay):
    print(f"[Task {name}] Starting (will fail in {delay}s)...")
    await asyncio.sleep(delay)
    print(f"[Task {name}] Failing now!")
    raise ValueError(f"Error in {name}")

# Run TaskGroup
async def run_task_group_demo():
    print("--- 1. TaskGroup Success Case ---")
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(task_success("A", 1))
        t2 = tg.create_task(task_success("B", 0.5))
    # Tasks are automatically awaited on exit of the block
    print("T1 Result:", t1.result())
    print("T2 Result:", t2.result())

    print("\n--- 2. TaskGroup Failure Case (Cancellation) ---")
    try:
        async with asyncio.TaskGroup() as tg:
            # Task C will start and run
            tg.create_task(task_success("C", 2.0))
            # Task D will fail quickly
            tg.create_task(task_failure("D", 0.5))
    except* ValueError as eg:
        # Python 3.11 ExceptionGroup handling
        print(f"Caught expected ExceptionGroup: {eg}")

# Run the async demo using standard event loop runner
# (We define a wrapper because we are running in an interactive python environment)
asyncio.run(run_task_group_demo())

# %% [markdown]
# ## 2. Worker Queue Distribution (asyncio.Queue)
# When coordinating producers (e.g. web scrapers, API endpoints) and consumers (e.g. database writers, file savers), `asyncio.Queue` provides a thread-safe, non-blocking FIFO pipe to distribute work.

# %%
async def worker(worker_id, queue):
    """Worker task that consumes items from the queue"""
    while True:
        # Get a work item from the queue
        item = await queue.get()
        try:
            print(f"[Worker {worker_id}] Processing item: {item}...")
            # Simulate CPU/IO bound processing time
            await asyncio.sleep(0.5)
            print(f"[Worker {worker_id}] Finished item: {item}")
        finally:
            # Notify the queue that the item has been fully processed
            queue.task_done()

async def run_queue_demo():
    # 1. Initialize queue
    queue = asyncio.Queue()

    # 2. Start consumer worker tasks in the background
    workers = []
    for i in range(2):  # 2 concurrent workers
        task = asyncio.create_task(worker(i, queue))
        workers.append(task)

    # 3. Producer: populate the queue with work items
    for item in ["Job_A", "Job_B", "Job_C", "Job_D"]:
        await queue.put(item)

    # 4. Wait until all items in the queue are fully processed
    await queue.join()
    print("All jobs completed successfully.")

    # 5. Cancel the background worker tasks since they loop infinitely
    for task in workers:
        task.cancel()
    
    # Wait for cancellation status to settle
    await asyncio.gather(*workers, return_exceptions=True)

asyncio.run(run_queue_demo())

# %% [markdown]
# ## 3. Async Synchronization (Event & Lock)
#
# - **`asyncio.Lock`**: Guarantees that only one coroutine can access a critical block (e.g. writing to a shared file or resource) at a time.
# - **`asyncio.Event`**: Coordinates multiple coroutines by allowing them to block/wait until a specific event flag is set (`event.set()`).

# %%
shared_resource = []
lock = asyncio.Lock()

async def safe_writer(coro_id):
    async with lock:  # Protect block
        print(f"[Writer {coro_id}] Acquired lock, writing to shared resource...")
        shared_resource.append(coro_id)
        await asyncio.sleep(0.1)
        print(f"[Writer {coro_id}] Done, releasing lock.")

async def waiter(event_id, event):
    print(f"[Waiter {event_id}] Waiting for system initialization event...")
    await event.wait()  # Block until event.set() is called
    print(f"[Waiter {event_id}] Event received! Starting execution.")

async def run_synchronization_demo():
    # 1. Test Lock
    print("--- 1. Testing asyncio.Lock ---")
    await asyncio.gather(safe_writer(1), safe_writer(2))
    print("Shared resource state:", shared_resource)

    # 2. Test Event
    print("\n--- 2. Testing asyncio.Event ---")
    system_ready = asyncio.Event()

    # Spawn waiters
    waiters = [asyncio.create_task(waiter(i, system_ready)) for i in range(2)]

    # Simulate database boot-up delay
    print("Booting system database...")
    await asyncio.sleep(1)
    
    # Trigger the event
    print("System database is ONLINE! Setting event.")
    system_ready.set()

    # Await waiters
    await asyncio.gather(*waiters)

asyncio.run(run_synchronization_demo())
