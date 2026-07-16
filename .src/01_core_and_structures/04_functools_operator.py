# %% [markdown]
# # Tutorial 04: Python Functools & Operator Modules
#
# Python supports functional programming paradigms. The `functools` module provides higher-order functions that interact with or return other functions, and the `operator` module provides efficient, built-in function equivalents to operators (like additions, item lookups, and attribute retrievals).
#
# In this notebook, we'll cover:
# 1. Metaprogramming with `@wraps`
# 2. Advanced Memoization (`@lru_cache` and `@cache`)
# 3. Partial Application (`partial` and `partialmethod`)
# 4. Function Overloading with `@singledispatch`
# 5. Clean & High-Performance Pipelines with the `operator` module

# %%
import time
from functools import wraps, lru_cache, cache, partial, singledispatch
import operator

# %% [markdown]
# ## 1. Preserving Metadata with @wraps
# When writing custom decorators, they wrap target functions. Without `@wraps`, the target function's metadata (docstring, name, annotations) is overwritten by the wrapper function's metadata.

# %%
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

def good_decorator(func):
    @wraps(func)  # Automatically copies docstring, name, etc.
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def greet_alice():
    """Greets Alice specifically."""
    return "Hello, Alice!"

@good_decorator
def greet_bob():
    """Greets Bob specifically."""
    return "Hello, Bob!"

# Inspecting metadata
print("greet_alice metadata (bad decorator):")
print("Name:", greet_alice.__name__)
print("Docstring:", greet_alice.__doc__)

print("\ngreet_bob metadata (good decorator):")
print("Name:", greet_bob.__name__)
print("Docstring:", greet_bob.__doc__)

# %% [markdown]
# ## 2. Advanced Caching & Memoization
# - `@lru_cache(maxsize=128)`: Caches calls based on arguments. If maxsize is reached, it discards the Least Recently Used entries.
# - `@cache`: An unbounded cache (equivalent to `lru_cache(maxsize=None)`). Fast and simple, introduced in Python 3.9.

# %%
@lru_cache(maxsize=4)
def expensive_calculation(n):
    print(f"Calculating {n}...")
    time.sleep(0.5)
    return n * n

# First runs (slow)
expensive_calculation(2)
expensive_calculation(3)
expensive_calculation(2)  # Instantly returns cached result!

# Check cache stats
print("\nCache Info:")
print(expensive_calculation.cache_info())

# Force clearing the cache
expensive_calculation.cache_clear()
print("\nCache Info after clear:")
print(expensive_calculation.cache_info())

# %% [markdown]
# ## 3. Partial Application (partial)
# `partial` freezes a subset of function arguments, creating a new callable with a simpler signature.

# %%
def power(base, exponent):
    return base ** exponent

# Create specialized functions
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print("Square of 5:", square(5))
print("Cube of 5:", cube(5))

# Using partial with built-ins (e.g. converting base-2 strings to int)
bintodec = partial(int, base=2)
print("Binary '1010' to int:", bintodec("1010"))

# %% [markdown]
# ## 4. Functional Overloading with @singledispatch
# Python doesn't support traditional function overloading by parameter types out of the box. `@singledispatch` transforms a function into a generic function that dispatches based on the type of its first argument.

# %%
@singledispatch
def format_data(data):
    """Fallback formatting function"""
    raise TypeError(f"Unsupported type: {type(data)}")

@format_data.register(str)
def _(data):
    return f"String: {data.upper()}"

@format_data.register(int)
def _(data):
    return f"Integer: {data:,} (Binary: {bin(data)})"

@format_data.register(list)
@format_data.register(tuple)
def _(data):
    return "Sequence: " + " -> ".join(format_data(item) for item in data)

# Test single dispatch
print(format_data("hello"))
print(format_data(1000000))
print(format_data(["test", 123]))

# %% [markdown]
# ## 5. High-Performance Selector Pipelines with operator
# Instead of slow lambda functions, the `operator` module provides C-implemented functions for common lookups.
# - `itemgetter`: Extracts items from index/key (like dictionaries or lists).
# - `attrgetter`: Extracts attributes from objects.
# - `methodcaller`: Calls a method on the passed object with arguments.

# %%
# Sort objects or dictionaries cleanly
students = [
    {"name": "Alice", "grade": 92},
    {"name": "Charlie", "grade": 85},
    {"name": "Bob", "grade": 95}
]

# Sort by grade using itemgetter (faster and cleaner than lambda x: x["grade"])
students.sort(key=operator.itemgetter("grade"))
print("Sorted by grade:", students)

# Retrieve specific fields using itemgetter
names_only = list(map(operator.itemgetter("name"), students))
print("Names only:", names_only)

# methodcaller example: execute upper() and replace() on list of strings
words = ["hello world", "python programming"]
upper_and_replace = operator.methodcaller("replace", " ", "_")
print("Modified strings:", [upper_and_replace(w.upper()) for w in words])
