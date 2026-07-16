# %% [markdown]
# # Tutorial 03: Python Concurrency (Threading vs Multiprocessing)
#
# Concurrency in Python is often misunderstood due to the Global Interpreter Lock (GIL). To write high-performance concurrent code, you must know when to use threads (via `threading` or `concurrent.futures`) and when to use processes (via `multiprocessing` or `concurrent.futures`).
#
# In this notebook, we'll cover:
# 1. CPU-bound vs. I/O-bound Workloads & GIL Basics
# 2. Multithreading & Thread Synchronization (`Lock`)
# 3. Multiprocessing & Inter-Process Communication (`Queue`)
# 4. High-Level Pools (`ThreadPoolExecutor` & `ProcessPoolExecutor`)

# %%
import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# %% [markdown]
# ## 1. CPU-bound vs. I/O-bound Workloads & GIL
#
# - **Global Interpreter Lock (GIL):** A mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once.
# - **I/O-bound Tasks:** Spend most of their time waiting for external resources (network, disk, user). The GIL is released during blocking I/O calls. Use **Threading**.
# - **CPU-bound Tasks:** Spend most of their time performing calculations. Threads cannot run concurrently on multiple cores due to the GIL. Use **Multiprocessing** to bypass the GIL by spawning separate OS processes.

# %%
def cpu_work(n):
    """Simulates CPU-bound task (calculating sum of squares)"""
    return sum(i * i for i in range(n))

def io_work(url):
    """Simulates I/O-bound task (downloading a page/sleeping)"""
    time.sleep(1)
    return f"Finished downloading {url}"

# %% [markdown]
# ## 2. Multithreading & Thread Synchronization
# When multiple threads modify shared mutable state, a **Race Condition** can occur. We must use locks to synchronize access.

# %%
shared_counter = 0
lock = threading.Lock()

def increment_without_lock():
    global shared_counter
    for _ in range(100000):
        # Read, increment, write are not atomic operations
        shared_counter += 1

def increment_with_lock():
    global shared_counter
    for _ in range(100000):
        # Acquire lock using context manager
        with lock:
            shared_counter += 1

# %% [markdown]
# ## 2. Multithreading & Thread Synchronization
# When multiple threads modify shared mutable state, a **Race Condition** can occur. We must use locks to synchronize access.

# %%
shared_counter = 0
lock = threading.Lock()

def increment_without_lock():
    global shared_counter
    for _ in range(100000):
        # Read, increment, write are not atomic operations
        shared_counter += 1

def increment_with_lock():
    global shared_counter
    for _ in range(100000):
        # Acquire lock using context manager
        with lock:
            shared_counter += 1

# %% [markdown]
# ## 3. Multiprocessing & Inter-Process Communication (IPC)
# Since processes have completely isolated memory spaces, they cannot share global variables easily. Instead, we use communication channels like `multiprocessing.Queue` or `Pipe`.

# %%
def worker_process(task_queue, result_queue):
    """Worker process pulling tasks and pushing results"""
    while True:
        try:
            # Non-blocking get with timeout to exit clean
            task = task_queue.get(timeout=1)
            result = cpu_work(task)
            result_queue.put((task, result))
        except:
            break

# %% [markdown]
# ## 4. High-Level Pools (concurrent.futures)
# The `concurrent.futures` module provides a high-level interface for asynchronously executing callables using pools of threads or processes.
#
# - `ThreadPoolExecutor`: Best for parallelizing I/O.
# - `ProcessPoolExecutor`: Best for parallelizing CPU-bound computation across multiple CPU cores.

# %% [markdown]
# ### Safe Multiprocessing & Execution
#
# **CRITICAL EXPERT TIP:** In Python, any script that spawns child processes (`multiprocessing` or `ProcessPoolExecutor`) MUST protect the entry point using `if __name__ == '__main__':`.
# Without this, spawning processes (especially on macOS/Windows using the `spawn` or `forkserver` start methods) will cause child processes to re-import the main script, causing infinite recursion or bootstrapping crashes.

# %%
if __name__ == '__main__':
    # --- Threading Demonstrations ---
    print("--- Running Threading Demos ---")
    shared_counter = 0
    t1 = threading.Thread(target=increment_without_lock)
    t2 = threading.Thread(target=increment_without_lock)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Counter without lock (expected 200000):", shared_counter)

    shared_counter = 0
    t3 = threading.Thread(target=increment_with_lock)
    t4 = threading.Thread(target=increment_with_lock)
    t3.start()
    t4.start()
    t3.join()
    t4.join()
    print("Counter with lock (expected 200000):", shared_counter)

    # --- Multiprocessing Queue Demo ---
    print("\n--- Running Multiprocessing Queue Demo ---")
    tasks = multiprocessing.Queue()
    results = multiprocessing.Queue()

    for num in [1_000_000, 2_000_000, 3_000_000]:
        tasks.put(num)

    processes = []
    for _ in range(2):
        p = multiprocessing.Process(target=worker_process, args=(tasks, results))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    while not results.empty():
        task, result = results.get()
        print(f"Task: {task} -> Result: {result}")

    # --- High-Level Pools (concurrent.futures) Demo ---
    print("\n--- Running concurrent.futures Pools Demo ---")
    urls = ["http://api1.com", "http://api2.com", "http://api3.com", "http://api4.com"]
    numbers_to_square = [5_000_000, 6_000_000, 7_000_000]

    # ThreadPoolExecutor for I/O tasks
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        io_results = list(executor.map(io_work, urls))
    print(f"I/O Thread Pool completed in {time.time() - start:.2f} seconds.")
    print("Results:", io_results)

    # ProcessPoolExecutor for CPU tasks
    start = time.time()
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(cpu_work, num) for num in numbers_to_square]
        cpu_results = [f.result() for f in futures]
    print(f"CPU Process Pool completed in {time.time() - start:.2f} seconds.")
    print("Results:", cpu_results)

