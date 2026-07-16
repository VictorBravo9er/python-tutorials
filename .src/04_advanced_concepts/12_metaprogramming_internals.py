# %% [markdown]
# # Tutorial 06: Python Metaprogramming & Custom Collections
#
# Metaprogramming is the technique of writing code that manipulates code. In Python, this is done using descriptors, dynamic class creation/validation, and implementing custom containers that hook perfectly into the language protocols.
#
# In this notebook, we'll cover:
# 1. Descriptors (`__get__` and `__set__` protocols)
# 2. Subclass Hooking via `__init_subclass__`
# 3. Metaclasses (`__new__` and custom classes)
# 4. Implementing Custom Collections using `collections.abc`

# %%
from collections.abc import MutableMapping
import re

# %% [markdown]
# ## 1. Descriptors: Behind the Scenes of Attributes
# A descriptor is an object attribute with "binding behavior", whose attribute access is overridden by methods in the descriptor protocol: `__get__`, `__set__`, and `__delete__`. If any of these methods are defined for an object, it is said to be a descriptor.
#
# Common descriptors include `@property`, `@classmethod`, and `@staticmethod`.
#
# Let's implement a validation descriptor to enforce numeric bounds.

# %%
class BoundedInteger:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val
        # Store data on the instance to keep it thread-safe and instance-isolated
        self.name = None

    def __set_name__(self, owner, name):
        """Automatically called when the containing class is created (Python 3.6+)"""
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, 0)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer.")
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"{self.name} must be between {self.min_val} and {self.max_val}.")
        instance.__dict__[self.name] = value


class GameCharacter:
    # Set descriptors
    health = BoundedInteger(0, 100)
    mana = BoundedInteger(0, 50)

    def __init__(self, name, health, mana):
        self.name = name
        self.health = health
        self.mana = mana

# Test descriptor validations
hero = GameCharacter("Arthur", 80, 20)
print(f"Character {hero.name} -> Health: {hero.health}, Mana: {hero.mana}")

try:
    hero.health = 150  # Over maximum limit
except ValueError as e:
    print("Caught expected validation error:", e)

# %% [markdown]
# ## 2. Class Hooking with __init_subclass__
# Introduced in Python 3.6, `__init_subclass__` provides a clean, readable alternative to metaclasses for tracking subclasses or validating class-level variables upon definition.

# %%
class PluginBase:
    # A class registry to track all active plugins
    registry = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name is None:
            raise ValueError("Subclasses must declare a 'plugin_name'")
        cls.registry[plugin_name] = cls

# Subclasses register automatically during class definition
class ImageFilterPlugin(PluginBase, plugin_name="image_filter"):
    def run(self):
        print("Filtering images...")

class TextSearchPlugin(PluginBase, plugin_name="text_search"):
    def run(self):
        print("Searching text...")

print("Registered Plugins:")
for name, cls in PluginBase.registry.items():
    print(f"- {name}: {cls.__name__}")

# %% [markdown]
# ## 3. Metaclasses: The Ultimate Blueprint
# A metaclass is the "class of a class". Standard classes define how instances behave, whereas metaclasses define how classes behave.
#
# Custom metaclasses are usually built by inheriting from `type`.

# %%
class UpperCaseAttributesMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Convert all user-defined methods and attributes to uppercase
        upper_namespace = {}
        for key, value in namespace.items():
            if not key.startswith("__"):  # Skip magic methods
                upper_namespace[key.upper()] = value
            else:
                upper_namespace[key] = value
        return super().__new__(mcs, name, bases, upper_namespace)


class AutomatedClass(metaclass=UpperCaseAttributesMeta):
    value = 42
    
    def greet(self):
        return "Hello!"

# Inspect attributes on class creation
obj = AutomatedClass()
print("\nInspecting attributes of AutomatedClass:")
print("Value (uppercase key):", getattr(obj, "VALUE"))
print("Greet method (uppercase key):", obj.GREET())

# %% [markdown]
# ## 4. Custom Containers with collections.abc
# If you want to create a custom dictionary-like or list-like class, you should inherit from Abstract Base Classes (ABCs) in `collections.abc`.
#
# By inheriting from `MutableMapping` and implementing only 5 abstract methods (`__getitem__`, `__setitem__`, `__delitem__`, `__iter__`, and `__len__`), Python will automatically generate the remaining dict interface methods like `.get()`, `.keys()`, `.values()`, `.items()`, `.pop()`, and `.setdefault()`.

# %%
class CaseInsensitiveDict(MutableMapping):
    """A dictionary that treats keys case-insensitively while preserving original casing."""
    def __init__(self, *args, **kwargs):
        self._store = {}
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __setitem__(self, key, value):
        # Store as lower_case_key -> (original_case_key, value)
        self._store[key.lower()] = (key, value)

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        # Iterate over original casing
        return (orig for orig, val in self._store.values())

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return f"{self.__class__.__name__}({dict(self.items())})"

# Test CaseInsensitiveDict
cid = CaseInsensitiveDict()
cid["Content-Type"] = "application/json"

# Key lookup is case-insensitive
print("\nCID Dict:", cid)
print("Lookup 'content-type':", cid["content-type"])
print("Lookup 'CONTENT-TYPE':", cid["CONTENT-TYPE"])

# Verify standard dictionary methods are automatically generated!
print("\nAutomatic methods supported:")
print("keys():", list(cid.keys()))
print("values():", list(cid.values()))
print("get('invalid', fallback):", cid.get("invalid", "Not Found"))
