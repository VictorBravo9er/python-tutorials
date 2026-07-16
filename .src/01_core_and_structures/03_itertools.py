# %% [markdown]
# # Tutorial 02: Python Advanced Itertools
#
# Python's `itertools` module is a collection of tools for handling iterators. It provides memory-efficient, fast looping tools that help write clean, pythonic code without building large intermediate lists in memory.
#
# In this notebook, we'll cover intermediate to expert usage of:
# 1. Infinite Iterators (`count`, `cycle`, `repeat`)
# 2. Terminating Iterators (`accumulate`, `groupby`, `islice`, `compress`, `dropwhile`, `takewhile`, `pairwise`, `zip_longest`)
# 3. Combinatoric Iterators (`product`, `permutations`, `combinations`, `combinations_with_replacement`)

# %%
import itertools
import operator

# %% [markdown]
# ## 1. Infinite Iterators
# These generate elements infinitely unless truncated.
#
# ### Key Functions:
# - `count(start, step)`: Infinite arithmetic progression.
# - `cycle(iterable)`: Cycles through an iterable indefinitely.
# - `repeat(object, times)`: Yields an object N times (or infinitely).

# %%
# Count starting at 10, step by 2.5
counter = itertools.count(10, 2.5)
print("count:")
for _ in range(4):
    print(next(counter))

# Cycle elements
cycler = itertools.cycle(["Red", "Green", "Blue"])
print("\ncycle:")
for _ in range(5):
    print(next(cycler))

# Repeat an item (useful for passing constants to map/zip)
repeater = itertools.repeat("Ping", 3)
print("\nrepeat:")
print(list(repeater))

# %% [markdown]
# ## 2. Terminating Iterators
# These process sequences and terminate based on the input iterator length or condition.
#
# ### Highlighted Functions:
# - `accumulate(iterable, func=operator.add)`: Accumulates values, customizable with binary functions.
# - `groupby(iterable, key=None)`: Groups consecutive items. **Crucial rule:** The input must be pre-sorted by the same key function.
# - `islice(iterable, start, stop, step)`: Slices any iterable without consuming/copying it fully.
# - `pairwise(iterable)`: Yields overlapping pairs of consecutive elements (Python 3.10+).
# - `zip_longest(*iterables, fillvalue=None)`: Zips until the longest iterable is exhausted.

# %%
# 1. Accumulate with custom operator (multiplication or custom lambda)
numbers = [1, 2, 3, 4, 5]
print("Running sum:", list(itertools.accumulate(numbers)))
print("Running product:", list(itertools.accumulate(numbers, operator.mul)))
print("Running max:", list(itertools.accumulate([2, 5, 1, 9, 3], max)))

# 2. Groupby - Groups consecutive matching items
data = [
    {"name": "Alice", "role": "Admin"},
    {"name": "Bob", "role": "User"},
    {"name": "Charlie", "role": "Admin"},
    {"name": "David", "role": "User"}
]

# CRITICAL: We must sort by the grouping key first!
key_func = lambda x: x["role"]
sorted_data = sorted(data, key=key_func)

print("\nGroupby results:")
for role, group in itertools.groupby(sorted_data, key=key_func):
    users_in_role = [user["name"] for user in group]
    print(f"Role: {role} -> Users: {users_in_role}")

# 3. Pairwise (adjacent pairs)
letters = "ABCDE"
print("\nPairwise:", list(itertools.pairwise(letters)))

# 4. Zip Longest
short = [1, 2]
long = ["a", "b", "c", "d"]
print("\nzip_longest (default fill):", list(itertools.zip_longest(short, long)))
print("zip_longest (custom fill):", list(itertools.zip_longest(short, long, fillvalue="MISSING")))

# %% [markdown]
# ## 3. Combinatoric Iterators
# Perfect for generating combinations and permutations efficiently.
#
# ### Key Functions:
# - `product(*iterables, repeat=1)`: Cartesian product (equivalent to nested for-loops).
# - `permutations(iterable, r=None)`: Ordered arrangements without duplicate elements.
# - `combinations(iterable, r)`: Unordered combinations in sorted order without replacement.
# - `combinations_with_replacement(iterable, r)`: Unordered combinations allowing repeated elements.

# %%
items = ["A", "B", "C"]

# Cartesian Product
print("Cartesian Product (repeat=2):", list(itertools.product([0, 1], repeat=2)))

# Permutations (Order matters: AB is different from BA)
print("\nPermutations of length 2:")
print(list(itertools.permutations(items, 2)))

# Combinations (Order doesn't matter: AB is the same as BA)
print("\nCombinations of length 2:")
print(list(itertools.combinations(items, 2)))

# Combinations with replacement (Allows AA, BB, CC)
print("\nCombinations with replacement of length 2:")
print(list(itertools.combinations_with_replacement(items, 2)))
