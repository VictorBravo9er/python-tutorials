# %% [markdown]
# # Tutorial 05: Contextlib & Dataclasses
#
# Clean resource management and structured data models are vital for robust Python software. In this notebook, we look at advanced techniques using:
# 1. `contextlib` (custom decorators, dynamic stacks, and exception silencing)
# 2. `dataclasses` (default factories, initialization validation, and immutability)

# %%
from contextlib import contextmanager, ExitStack, suppress
from dataclasses import dataclass, field
from typing import List

# %% [markdown]
# ## 1. contextlib: Advanced Resource Management
# While `with open(...)` is standard, we can build custom context managers easily using the `@contextmanager` decorator, and handle complex multi-resource setups with `ExitStack`.

# %%
# 1. Custom context manager using a generator
@contextmanager
def transaction(db_conn):
    print("[TX] Starting Transaction...")
    try:
        yield db_conn  # The block inside the 'with' statement runs here
        print("[TX] Committing Transaction!")
    except Exception as e:
        print(f"[TX] Error detected: {e}. Rolling back!")
        raise

# Test transaction behavior
fake_conn = "DatabaseConnectionObject"
print("--- Success Scenario ---")
with transaction(fake_conn) as conn:
    print("Writing data to:", conn)

print("\n--- Failure Scenario ---")
try:
    with transaction(fake_conn) as conn:
        print("Writing data...")
        raise ValueError("Invalid record")
except ValueError:
    print("Caught error in outer scope")


# 2. Silencing predictable exceptions with suppress
print("\n--- Suppressing Exceptions ---")
with suppress(FileNotFoundError):
    # This file doesn't exist, but it won't crash the script
    with open("non_existent_file.txt", "r") as f:
        pass
print("Execution continued normally after suppression.")


# 3. Dynamic resource handling with ExitStack
# Useful when opening an arbitrary number of resources (e.g., dynamically matched file handlers)
print("\n--- Dynamic Context Handling with ExitStack ---")
files_to_read = ["/etc/hosts", "/etc/resolv.conf"]
with ExitStack() as stack:
    # Safely open all files; if one fails, it automatically cleans up the already-opened ones
    file_objects = [stack.enter_context(open(name, "r")) for name in files_to_read]
    print(f"Opened {len(file_objects)} system files simultaneously.")
    # Check lines of the first file
    print("First line of hosts:", file_objects[0].readline().strip())

# %% [markdown]
# ## 2. dataclasses: Typed Data Containers
# Python's `dataclass` module automates the generation of boilerplate methods (like `__init__`, `__repr__`, `__eq__`) on classes.
#
# ### Advanced Dataclass Concepts:
# - `field(default_factory=...)`: Required for mutable defaults (lists, dicts).
# - `__post_init__`: Executed immediately after `__init__` for custom calculations or attribute validation.
# - `frozen=True`: Creates read-only, hashable objects.

# %%
@dataclass(frozen=True)
class ImmutableConfig:
    host: str
    port: int = 8000

config = ImmutableConfig("127.0.0.1")
print("Config object:", config)
try:
    config.port = 9000  # Will raise FrozenInstanceError
except Exception as e:
    print("Error updating frozen object:", type(e).__name__)


@dataclass
class Team:
    name: str
    # CRITICAL: Do NOT use members: List[str] = [] (mutable defaults are disallowed)
    members: List[str] = field(default_factory=list)
    manager: str = "Unassigned"
    description: str = field(init=False)  # Exclude from generated __init__ constructor

    def __post_init__(self):
        """Custom validation and initialization logic"""
        # Validate input
        if not self.name.strip():
            raise ValueError("Team name cannot be empty")
        
        # Calculate derived fields
        self.description = f"Team '{self.name}' managed by {self.manager} ({len(self.members)} members)"

# Create a Team
dev_team = Team(name="Engineering", members=["Alice", "Bob"], manager="Charlie")
print("\nTeam Object:", dev_team)
print("Derived Description:", dev_team.description)

# Demonstration of default_factory isolation
other_team = Team(name="Marketing")
print("\nOther Team members:", other_team.members)  # Empty list, unaffected by dev_team
