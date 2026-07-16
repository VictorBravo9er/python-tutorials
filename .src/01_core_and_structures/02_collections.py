# %% [markdown]
# # Tutorial 01: Python Advanced Collections
#
# Python's built-in `collections` module provides specialized container datatypes that serve as high-performance alternatives to the general-purpose built-ins like `dict`, `list`, `set`, and `tuple`.
#
# In this notebook, we'll dive deep into intermediate to expert features of:
# 1. `Counter` (Multisets & Mathematical Operations)
# 2. `defaultdict` (Automatic Initialization & Custom Factories)
# 3. `deque` (Thread-safe Double-ended Queues with `maxlen`)
# 4. `NamedTuple` (Modern Typed Structures)
# 5. `ChainMap` (Stacked Scope Lookups)
# 6. `OrderedDict` (Order-sensitive Dict & LRU Cache Helpers)

# %%
from collections import Counter, defaultdict, deque, ChainMap, OrderedDict
from typing import NamedTuple

# %% [markdown]
# ## 1. Counter: More Than Just Counting
# A `Counter` is a dictionary subclass for counting hashable objects. It is a mathematical multiset (a set that allows duplicate elements).
#
# ### Advanced Counter Operations:
# - Finding the most common elements (`most_common`).
# - Arithmetic operations: Union (`|`), Intersection (`&`), Addition (`+`), and Subtraction (`-`).
# - Elements expansion and in-place updates.

# %%
# Basic counting
char_counts = Counter("abracadabra")
print("Initial counter:", char_counts)

# Retrieve N most common elements (returns list of tuples)
print("Top 2 common:", char_counts.most_common(2))

# Subtraction and Addition of Counts
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2, c=4)

print("\nc1:", c1)
print("c2:", c2)
print("Addition (c1 + c2):", c1 + c2)
print("Subtraction (c1 - c2 - keeps only positive counts):", c1 - c2)
print("Intersection (min counts, &):", c1 & c2)
print("Union (max counts, |):", c1 | c2)

# Expanding a Counter back to an iterator of elements
print("Elements in c1:", list(c1.elements()))

# %% [markdown]
# ## 2. defaultdict: Dynamic Value Instantiation
# `defaultdict` is a dict subclass that calls a factory function to supply missing values.
#
# ### Advanced Behavior:
# - Using standard callables (`list`, `set`, `int`).
# - Custom factory functions for complex structures or default initialization logic.

# %%
# Grouping elements into a list
grouped = defaultdict(list)
data = [("fruit", "apple"), ("vegetable", "carrot"), ("fruit", "banana")]
for category, item in data:
    grouped[category].append(item)
print("Grouped by list:", dict(grouped))

# Custom factory function (e.g. default value of a dict with a pre-configured nested dict)
def default_user():
    return {"status": "inactive", "role": "guest"}

users = defaultdict(default_user)
users["alice"]["status"] = "active"  # 'alice' did not exist, but default_user() was invoked
print("\nUsers database:")
print("Alice:", users["alice"])
print("Bob (accessed but not modified):", users["bob"])

# %% [markdown]
# ## 3. deque: High-Performance Double-Ended Queue
# `deque` (double-ended queue) is designed for fast, O(1) appends and pops from both ends. Unlike lists, which have O(N) complexity for insertions and deletions at the front.
#
# ### Key Features:
# - `maxlen`: Creates a bounded queue. Once full, adding elements to one side discards elements from the opposite side.
# - Rotation (`rotate`): Rotates elements circularly.

# %%
# Create a bounded deque
history = deque(maxlen=3)
for i in range(5):
    history.append(i)
    print(f"Added {i} -> Current deque: {list(history)}")

# Appending and popping from left
q = deque([1, 2, 3])
q.appendleft(0)
q.append(4)
print("\nDeque:", q)
print("Popped left:", q.popleft())
print("Popped right:", q.pop())
print("After pops:", q)

# Rotating elements
rotator = deque([1, 2, 3, 4, 5])
rotator.rotate(2)  # Shift 2 steps to the right
print("\nRotated right by 2:", rotator)
rotator.rotate(-1)  # Shift 1 step to the left
print("Rotated left by 1:", rotator)

# %% [markdown]
# ## 4. NamedTuple: Typed & Immutable Data Containers
# `NamedTuple` from the `typing` module brings structure, immutability, and type safety to traditional tuples.
#
# ### Benefits:
# - Memory-efficient alternative to class objects.
# - Unpacking and indexability of tuples.
# - Clean typing support.

# %%
class Point(NamedTuple):
    x: float
    y: float
    label: str = "Origin"  # Fields can have default values

p1 = Point(10.5, 20.0)
p2 = Point(0.0, 0.0, label="Start")

print("Point 1:", p1)
print("Access by attribute:", p1.x, p1.label)
print("Access by index:", p1[0], p1[2])

# NamedTuples are immutable, but we can replace values to create new instances
p3 = p1._replace(x=15.0)
print("Modified Point (new instance):", p3)

# Conversion to dict
print("As dictionary:", p1._asdict())

# %% [markdown]
# ## 5. ChainMap: Managing Stacked Scopes
# A `ChainMap` groups multiple dictionaries or mappings together to create a single, updatable view.
#
# ### Typical Use Case:
# Command line arguments overriding environment variables, which in turn override configuration defaults.

# %%
defaults = {"theme": "light", "show_tips": True, "port": 8080}
env_vars = {"theme": "dark", "port": 3000}
cli_args = {"port": 5000}

# Create a ChainMap (order defines lookup precedence: left to right)
config = ChainMap(cli_args, env_vars, defaults)

print("Looked up port (CLI precedence):", config["port"])
print("Looked up theme (Env precedence):", config["theme"])
print("Looked up show_tips (Defaults fallback):", config["show_tips"])

# Updating the ChainMap updates the FIRST mapping in the chain
config["theme"] = "blue"
print("\nAfter updating 'theme':")
print("CLI args dict:", cli_args)
print("Entire ChainMap:", config)

# Creating a new child scope
nested_config = config.new_child({"port": 9000})
print("\nNested Config (new child):", nested_config)
print("Nested Port:", nested_config["port"])
print("Parent Port:", nested_config.parents["port"])

# %% [markdown]
# ## 6. OrderedDict: Order-Sensitive Dicts
# In Python 3.7+, standard dictionaries preserve insertion order. However, `OrderedDict` remains highly useful due to specific behaviors:
#
# ### Advanced OrderedDict Features:
# - Reordering: `move_to_end(key, last=True)` moves an item to either end.
# - Equality comparison: `OrderedDict` is order-sensitive when comparing equality (`==`). Standard dictionaries are NOT.

# %%
d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
print("Standard Dicts equal?", d1 == d2)

od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
print("OrderedDicts equal?", od1 == od2)

# Move to end demonstration (ideal for implementing LRU caches manually)
cache = OrderedDict()
cache["page1"] = "content1"
cache["page2"] = "content2"
cache["page3"] = "content3"

# Access page1, making it the most recently used (move to the end)
cache.move_to_end("page1")
print("\nCache after moving 'page1' to end:", list(cache.keys()))

# Evict the oldest item (first item)
oldest_key, oldest_val = cache.popitem(last=False)
print(f"Evicted oldest: {oldest_key} -> {oldest_val}")
print("Remaining cache:", list(cache.keys()))
