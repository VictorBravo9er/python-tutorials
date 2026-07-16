# %% [markdown]
# # Tutorial 09: Advanced Typing & Regular Expressions
#
# Python's standard library provides incredibly powerful tools for type-safety and text processing.
# In this notebook, we'll dive deep into:
# 1. Advanced `typing` patterns (`Protocol`, custom `Generic` classes, `TypeGuard`, `ParamSpec`, and `Self`).
# 2. Advanced `re` patterns (named groups, lookaround assertions, and verbose regex mode).

# %%
import re
from typing import (
    TypeVar, Generic, Protocol, TypeGuard, ParamSpec, Callable, Self, List, Any
)

# %% [markdown]
# ## 1. Advanced Typing Systems
#
# ### Key Concepts:
# - **`Protocol` (Structural Subtyping / Duck Typing):** Defines an interface that classes can satisfy implicitly without inheriting from it.
# - **`Generic` & `TypeVar`:** Builds structures that can work with any specified type while maintaining type constraints.
# - **`TypeGuard`:** Declares type narrowing functions that help type checkers infer types within conditional branches.
# - **`ParamSpec`:** Preserves the parameter signature of decorated functions.
# - **`Self`:** Denotes the type of the current enclosing class, which is perfect for fluent APIs (method chaining).

# %%
# 1. Structural Subtyping with Protocol
class Renderable(Protocol):
    def render(self) -> str:
        ...

def display(item: Renderable) -> None:
    print(item.render())

class Article:
    def render(self) -> str:
        return "Article rendered content."

class Image:
    # No explicit subclassing of Renderable, but satisfies the Protocol!
    def render(self) -> str:
        return "<Image Asset>"

display(Article())
display(Image())


# 2. Custom Generics
T = TypeVar("T")

class Repository(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def get_all(self) -> List[T]:
        return self._items

# Type-safe Repository of strings
str_repo = Repository[str]()
str_repo.add("Alice")
print("\nRepository Items:", str_repo.get_all())


# 3. Type narrowing with TypeGuard
def is_str_list(val: List[Any]) -> TypeGuard[List[str]]:
    """Returns True if all elements in the list are strings"""
    return all(isinstance(x, str) for x in val)

mixed_list: List[Any] = ["apple", "banana", "cherry"]
if is_str_list(mixed_list):
    # Within this block, static analyzers know mixed_list is List[str]
    print("Checked List:", [s.upper() for s in mixed_list])


# 4. Fluent API using Self (Python 3.11+)
class QueryBuilder:
    def __init__(self) -> None:
        self.query = "SELECT * FROM users"

    def filter_by(self, column: str, value: str) -> Self:
        self.query += f" WHERE {column} = '{value}'"
        return self

    def limit(self, count: int) -> Self:
        self.query += f" LIMIT {count}"
        return self

qb = QueryBuilder().filter_by("role", "admin").limit(5)
print("\nGenerated Query:", qb.query)

# %% [markdown]
# ## 2. Advanced Regular Expressions (re)
# Regular expressions are a core tool for text extraction. Beyond basic matching, expert pythonistas utilize named groups, lookarounds, and verbose layout modes.
#
# ### Advanced Patterns:
# - **Named Groups `(?P<name>pattern)`**: Assigns a readable name to matching substrings.
# - **Lookaround Assertions**: Matches patterns based on what precedes or follows them without including those characters in the matched string:
#   - Lookahead: Positive `(?=...)`, Negative `(?!...)`
#   - Lookbehind: Positive `(?<=...)`, Negative `(?<!...)`
# - **Verbose Regex `re.VERBOSE`**: Allows inserting spaces and comments inside the regex string for maximum readability.

# %%
# 1. Named Groups
log_entry = "2026-07-16 08:30:15 [ERROR] Database connection failed"
log_pattern = r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) \[(?P<level>\w+)\] (?P<message>.*)"

match = re.match(log_pattern, log_entry)
if match:
    print("Named Group Matches:")
    print("Date:", match.group("date"))
    print("Level:", match.group("level"))
    print("Message:", match.group("message"))
    print("Dictionary representation:", match.groupdict())


# 2. Lookaround Assertions
# Match prices (e.g. 100) ONLY if preceded by '$' (Positive Lookbehind)
prices = "The items cost $100, €80, and $45."
dollar_amounts = re.findall(r"(?<=\$)\d+", prices)
print("\nDollar amounts (lookbehind):", dollar_amounts)

# Match words NOT followed by a period (Negative Lookahead)
text = "Run. Stop. Go now"
words_no_period = re.findall(r"\b\w+\b(?! \w+\.)", text)
print("Words not followed by period (lookahead):", words_no_period)


# 3. Verbose Regular Expressions (re.VERBOSE)
# Simplifies writing complex patterns with comments
phone_text = "Call me at 123-456-7890 or 987-654-3210."

# Complex regex cleanly documented
phone_pattern = re.compile(r"""
    \b(?P<area>\d{3})  # Area code (3 digits)
    -                  # Separator
    (?P<prefix>\d{3})  # Prefix code (3 digits)
    -                  # Separator
    (?P<line>\d{3,4})  # Line number (3 to 4 digits)
    \b
""", re.VERBOSE)

for match in phone_pattern.finditer(phone_text):
    print(f"\nPhone Match: {match.group(0)}")
    print(f"  Area: {match.group('area')}, Prefix: {match.group('prefix')}, Line: {match.group('line')}")
