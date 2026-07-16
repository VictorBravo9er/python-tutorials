# %% [markdown]
# # The Zen of Python: Applied (Extended Edition)
# Execute each cell. Read the critiques carefully. Your code must be a precise tool, not a liability.

# %% [markdown]
# ### 1. Beautiful is better than ugly.
# **Critique:** Ugly code creates cognitive load. When another engineer (or you in six months) reads your script, they should immediately grasp the logic without parsing visual clutter. Disorganized code masks logical flaws and slows down reviews.
# **Action:** Enforce strict formatting, standard whitespace, and logical groupings.

# %%
# BAD 1: Crammed logic.
def calc(a, b, c):
    return a + b * c


# GOOD 1: Clean spacing and naming.
def calculate_total(base, tax, multiplier):
    return base + (tax * multiplier)


# BAD 2: Visually dense data structures.
config = {"env": "prod", "timeout": 30, "retry": 3, "log_level": "debug", "workers": 4}

# GOOD 2: Vertical alignment for immediate scanning.
config = {"env": "prod", "timeout": 30, "retry": 3, "log_level": "debug", "workers": 4}

# %% [markdown]
# ### 2. Explicit is better than implicit.
# **Critique:** Magic behaviors, implied variable scopes, and blind assumptions create untrackable bugs. Your code must explicitly state its inputs, outputs, and dependencies. If I have to guess where a variable came from, your architecture is flawed.
# **Action:** Declare exact imports. Define required arguments instead of blindly catching catch-alls.

# %%
# BAD 1: Pollutes the namespace.
from math import *

x = sqrt(4)

# GOOD 1: The origin is undeniable.
import math

x = math.sqrt(4)


# BAD 2: Implicit arguments. What does this function actually need?
def process_user(**kwargs):
    print(f"Processing {kwargs.get('username')}")


# GOOD 2: Explicit arguments. The requirements are absolute.
def process_user_strict(username: str, email: str, active: bool = True):
    print(f"Processing {username}")


# %% [markdown]
# ### 3 & 4. Simple is better than complex. Complex is better than complicated.
# **Critique:** Do not over-engineer solutions to show off. A simple loop is superior to a convoluted class hierarchy. However, if the business logic is inherently difficult (complex), structure it logically. Do not build a messy, tangled web of cross-dependencies (complicated).
# **Action:** Default to built-in functions. Only build classes when state must be maintained.

# %%
# BAD 1: Complicated approach to a simple problem.
words = ["python", "is", "efficient"]
lengths = []
for i in range(len(words)):
    lengths.append(len(words[i]))

# GOOD 1: Simple and Pythonic.
lengths = [len(word) for word in words]


# BAD 2: Over-engineered class for a single action.
class Greeter:
    def __init__(self, name):
        self.name = name

    def execute(self):
        return f"Hello, {self.name}"


# GOOD 2: A simple function for a simple action.
def greet(name: str) -> str:
    return f"Hello, {name}"


# %% [markdown]
# ### 5 & 6. Flat is better than nested. Sparse is better than dense.
# **Critique:** The "Arrow Anti-Pattern" (code indented halfway across the screen) is a sign of poor structural planning. It is physically difficult to read. Furthermore, dense one-liners that do five things at once are impossible to step through in a debugger.
# **Action:** Use guard clauses to return early and eliminate `else` blocks. Split multi-operation lines.


# %%
# BAD 1: Deeply nested.
def process_data(data):
    if data:
        if isinstance(data, list):
            for item in data:
                if item > 0:
                    print(item * 2)


# GOOD 1: Guard clauses keep it flat.
def process_data_flat(data):
    if not isinstance(data, list):
        return
    for item in data:
        if item > 0:
            print(item * 2)


# BAD 2: Unreadably dense logic.
data = [{"val": 10, "act": True}, {"val": -5, "act": True}, {"val": 20, "act": False}]
res = [x["val"] * 2 for x in data if x["act"] and x["val"] > 0]  # Too much happening.

# GOOD 2: Sparse and debuggable.
valid_items = (x["val"] for x in data if x["act"] and x["val"] > 0)
res = [val * 2 for val in valid_items]

# %% [markdown]
# ### 7. Readability counts.
# **Critique:** You write code once, but it is read hundreds of times. Code is communication. Using single-letter variables or confusing abbreviations is lazy and negligent.
# **Action:** Name variables exactly what they represent. Rely on Python's truthiness for clean evaluations.

# %%
# BAD 1: Cryptic abbreviations.
t = 86400
d = t / 3600

# GOOD 1: Self-documenting variables.
SECONDS_IN_DAY = 86400
hours_in_day = SECONDS_IN_DAY / 3600

# BAD 2: Unreadable boolean checks.
items = []
if len(items) == 0:
    print("Empty")

# GOOD 2: Clean, readable truthiness.
if not items:
    print("Empty")

# %% [markdown]
# ### 8 & 9. Special cases aren't special enough to break the rules. Although practicality beats purity.
# **Critique:** Consistency across a codebase is paramount. You are not a unique exception. However, if strict adherence to a rule severely degrades performance or causes catastrophic unreadability, you must be practical.
# **Action:** Stick to standard patterns 99% of the time.


# %%
# BAD 1: Breaking standard types for a "clever" one-off exception.
def add_items(item, item_list=""):
    if not item_list:
        item_list = []  # Mixed types are a nightmare.
    item_list.append(item)


# GOOD 1: Practical and consistent.
def add_items_clean(item, item_list=None):
    if item_list is None:
        item_list = []
    item_list.append(item)


# BAD 2: Over-purist type checking that breaks duck typing.
def process_sequence(seq):
    if type(seq) == list or type(seq) == tuple:  # Too rigid.
        print(len(seq))


# GOOD 2: Practical duck typing. Let it fail if it doesn't have __len__.
def process_sequence_clean(seq):
    try:
        print(len(seq))
    except TypeError:
        print("Sequence has no length.")


# %% [markdown]
# ### 10 & 11. Errors should never pass silently. Unless explicitly silenced.
# **Critique:** Swallowing errors with a bare `except: pass` is malicious incompetence. It hides systemic failures and prevents diagnosis.
# **Action:** Catch specific exceptions. If you intentionally ignore one, log it or comment exactly why.

# %%
# BAD 1: Suppresses everything, including system exits.
try:
    1 / 0
except:
    pass

# GOOD 1: Targeted handling.
try:
    1 / 0
except ZeroDivisionError:
    print("Handled division by zero.")


# BAD 2: Catching a specific error but hiding the trace entirely.
def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return ""  # Dangerous. Did the file fail to load, or is it empty?


# GOOD 2: Explicit logging if an error is silenced.
import logging


def read_file_safe(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        logging.warning(f"File missing, returning empty string: {e}")
        return ""


# %% [markdown]
# ### 12. In the face of ambiguity, refuse the temptation to guess.
# **Critique:** If an input's type, value, or intent is uncertain, do not write logic that attempts to "guess" what the user meant. Guessing leads to unpredictable edge cases and corrupted data.
# **Action:** Fail fast. Throw an exception or enforce strict requirements.


# %%
# BAD 1: Guessing that a string "5" should be an integer.
def multiply_by_two(val):
    if type(val) == str:
        val = int(val)
    return val * 2


# GOOD 1: Strict enforcement.
def multiply_by_two_strict(val: int) -> int:
    if not isinstance(val, int):
        raise TypeError("val must be an integer")
    return val * 2


# BAD 2: Guessing a critical default value.
def assign_role(user_data):
    role = user_data.get("role", "admin")  # Never guess default permissions.


# GOOD 2: Let it fail if the data is missing.
def assign_role_strict(user_data):
    role = user_data["role"]  # Raises KeyError if undefined.


# %% [markdown]
# ### 13 & 14. There should be one-- and preferably only one --obvious way to do it.
# **Critique:** Python has idiomatic ways of solving problems. Reinventing the wheel shows a lack of platform knowledge.
# **Action:** Learn the standard library. Use standard idioms.

# %%
# BAD 1: Manual dictionary merging.
d1, d2 = {"a": 1}, {"b": 2}
d3 = {}
for k, v in d1.items():
    d3[k] = v
for k, v in d2.items():
    d3[k] = v

# GOOD 1: The obvious, idiomatic way.
d3 = d1 | d2

# BAD 2: Manual index tracking.
items = ["a", "b", "c"]
for i in range(len(items)):
    print(i, items[i])

# GOOD 2: Built-in enumeration.
for index, item in enumerate(items):
    print(index, item)

# %% [markdown]
# ### 15 & 16. Now is better than never. Although never is often better than *right* now.
# **Critique:** Endless planning ("analysis paralysis") yields zero value. However, pushing untested, half-baked code to production causes outages.
# **Action:** Build the core logic immediately, but do not deploy until validation, tests, and guards are strictly implemented.


# %%
# BAD 1: Pushing raw input to a DB immediately.
def save_user(username):
    # db.execute(f"INSERT INTO users VALUES ('{username}')") # SQL Injection risk.
    pass


# GOOD 1: Ship it now, but guarded.
def save_user_safe(username: str):
    if not username.isalnum():
        raise ValueError("Invalid username")
    # db.execute("INSERT INTO users VALUES (?)", (username,))


# BAD 2: Premature optimization (Never finishing).
def complex_sort(data):
    # Spending 40 hours writing a custom C-extension for a 100-item list.
    pass


# GOOD 2: Ship the naive solution now, profile later.
def simple_sort(data):
    return sorted(data)


# %% [markdown]
# ### 17 & 18. If the implementation is hard to explain, it's a bad idea.
# **Critique:** Code is a collaborative asset. If you cannot explain your algorithm clearly in two sentences, it is poorly designed. Opaque, "clever" code is technical debt.
# **Action:** Refactor complex logic into distinct steps. Standardize operations.

# %%
# BAD 1: Opaque recursive lambda.
f = lambda n: 1 if n <= 1 else n * f(n - 1)


# GOOD 1: Clear, documented function.
def calculate_factorial(n: int) -> int:
    """Returns the factorial of n."""
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)


# BAD 2: Massive, unreadable regex to extract a domain.
import re


def get_domain(url):
    return re.match(r"^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)", url).group(
        1
    )


# GOOD 2: Utilizing standard libraries that are easy to explain.
from urllib.parse import urlparse


def get_domain_clean(url):
    return urlparse(url).netloc


# %% [markdown]
# ### 19. Namespaces are one honking great idea -- let's do more of those!
# **Critique:** Dumping variables and functions into the global scope guarantees naming collisions and unpredictable side effects.
# **Action:** Encapsulate logic inside specific functions, classes, or cleanly imported modules.

# %%
# BAD 1: Global scope manipulation.
status = "active"


def update_status():
    global status
    status = "inactive"


# GOOD 1: Class encapsulation.
class Job:
    def __init__(self):
        self.status = "active"

    def cancel(self):
        self.status = "inactive"


# BAD 2: Star imports pollute the local namespace.
# from datetime import *
# today = date.today()

# GOOD 2: Explicit module referencing preserves the namespace.
import datetime

today = datetime.date.today()

# %% [markdown]
# # Pythonic Philosophy: EAFP (Easier to Ask for Forgiveness than Permission)
# Python's exception handling is fast. Constantly checking if something is valid before doing it wastes resources and creates race conditions.

# %% [markdown]
# ### The Philosophy: Just do it, handle the failure.
# **Critique:** The "Look Before You Leap" (LBYL) approach clutters your codebase with `if/else` statements. Worse, it introduces race conditions. If you check if a file exists, and another process deletes that file a millisecond before you open it, your program will still crash.
# **Action:** Assume the operation will succeed. Use a `try/except` block to catch the specific failure (the "apology").

# %%
# BAD 1: LBYL (Look Before You Leap) - Dictionary access.
# This requires querying the dictionary twice: once to check, once to access.
user_data = {"name": "Alice", "role": "admin"}

if "age" in user_data:
    age = user_data["age"]
else:
    age = "Unknown"

# GOOD 1: EAFP (Easier to Ask for Forgiveness than Permission).
# Query the dictionary exactly once. Catch the error if it fails.
try:
    age = user_data["age"]
except KeyError:
    age = "Unknown"

# NOTE: For dictionaries specifically, the `.get()` method is the most Pythonic abstraction of this.
# age = user_data.get("age", "Unknown")

# %%
# BAD 2: LBYL - File I/O.
# Checking if a file exists before opening it is a classic race condition.
import os

file_path = "data.txt"

if os.path.exists(file_path):
    # What if another process deletes data.txt right... NOW?
    with open(file_path, "r") as file:
        data = file.read()
else:
    data = "Default Data"

# GOOD 2: EAFP - File I/O.
# Attempt the operation immediately. The OS handles the lock and state simultaneously.
try:
    with open(file_path, "r") as file:
        data = file.read()
except FileNotFoundError:
    data = "Default Data"

# %% [markdown]
# ### A Warning Against Extreme EAFP
# **Critique:** EAFP is not an excuse to write sloppy logic or mask fundamental system errors. If an error is highly probable or represents a core logic branch, `try/except` blocks can become expensive and obscure intent.
# **Action:** Use EAFP for I/O operations, dictionary lookups, and attribute access. Do not use it to control fundamental business logic flow.


# %%
# BAD: Using EAFP for basic logic flow where LBYL is mathematically superior.
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 0


# GOOD: Strict, readable evaluation.
def divide_strict(a, b):
    if b == 0:
        return 0
    return a / b


# %% [markdown]
# # Advanced Pythonic Philosophies
# Execute these cells to distinguish between native Python design and imported paradigms from other languages.

# %% [markdown]
# ### 1. Duck Typing: Focus on Behavior, Not Lineage
# **Critique:** Obsessively checking if an object is an exact class instance (e.g., using `type()` or `isinstance()`) creates brittle, inflexible code. It breaks polymorphism. If an object behaves like the type you need—if it "walks like a duck and quacks like a duck"—treat it as a duck.
# **Action:** Rely on the object's methods. If a function requires a file, do not check if it is an `io.TextIOWrapper`; just call `.read()`.

# %%
# BAD: Rigid type checking. This rejects valid mock objects or custom stream classes.
import io


def process_data_stream(stream):
    if not isinstance(stream, (io.StringIO, io.TextIOWrapper)):
        raise TypeError("Expected a valid text stream")
    return stream.read().upper()


# GOOD: Duck Typing. Trust the interface. If it lacks .read(), EAFP will catch the AttributeError.
def process_data_stream_clean(stream):
    try:
        return stream.read().upper()
    except AttributeError:
        raise TypeError("Expected an object with a .read() method")


# %% [markdown]
# ### 2. YAGNI (You Aren't Gonna Need It)
# **Critique:** Anticipating features that do not exist yet creates bloated, highly abstract architecture. This is a severe form of technical debt. It confuses current developers for the sake of future requirements that rarely materialize.
# **Action:** Build exactly what the business logic dictates today. Do not write base classes, factories, or interfaces for single implementations.


# %%
# BAD: Over-engineered architecture for a single current requirement.
class AbstractDataWriter:
    def write(self, data):
        raise NotImplementedError


class CSVWriter(AbstractDataWriter):
    def write(self, data):
        print(f"Writing {data} to CSV")


class WriterFactory:
    @staticmethod
    def get_writer(writer_type):
        if writer_type == "csv":
            return CSVWriter()
        raise ValueError("Unknown writer")


# GOOD: Direct, immediate implementation. Refactor to a class only when a second format is actually required.
def write_csv(data, filepath):
    print(f"Writing {data} to {filepath}")


# %% [markdown]
# ### 3. Embrace the Data Model (Dunder Methods)
# **Critique:** Forcing Java-style getter/setter paradigms or custom methods like `get_size()` onto Python classes ignores the built-in protocols of the language. It forces other developers to memorize your custom API instead of using standard Python functions.
# **Action:** Implement double-underscore ("dunder") methods like `__len__`, `__getitem__`, and `__str__`. Make your custom objects interact seamlessly with native functions like `len()` and `for` loops.


# %%
# BAD: Non-idiomatic custom API.
class ShoppingCart:
    def __init__(self):
        self.items = ["apple", "banana"]

    def get_count(self):
        return len(self.items)

    def get_item_at(self, index):
        return self.items[index]


cart = ShoppingCart()
# Developers have to memorize your arbitrary method names.
print(cart.get_count())
print(cart.get_item_at(0))


# GOOD: Pythonic integration with the Data Model.
class ShoppingCartPythonic:
    def __init__(self):
        self.items = ["apple", "banana"]

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]


pythonic_cart = ShoppingCartPythonic()
# Developers use standard Python syntax. No memorization required.
print(len(pythonic_cart))
print(pythonic_cart[0])
for item in pythonic_cart:
    pass  # Iteration works automatically via __getitem__

# %% [markdown]
# ### 4. Comprehensions over Functional Primitives
# **Critique:** While `map()` and `filter()` exist in Python, combining them with `lambda` functions often yields unreadable code. Python comprehensions were explicitly designed to replace this functional clutter with clean, declarative syntax.
# **Action:** Use list, dictionary, and set comprehensions for mapping and filtering data.

# %%
# BAD: Cluttered functional syntax that is difficult to parse visually.
numbers = [1, 2, 3, 4, 5, 6]
squared_evens = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))

# GOOD: A highly readable, standard list comprehension.
squared_evens_clean = [x**2 for x in numbers if x % 2 == 0]
