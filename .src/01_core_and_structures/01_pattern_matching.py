# %% [markdown]
# # Tutorial 01: Structural Pattern Matching (match-case)
#
# Python 3.10 introduced **Structural Pattern Matching** (`match-case`). While it looks like a traditional switch-case statement from other languages, it is far more powerful. It allows matching complex data structures, checking types, extracting internal variables, and evaluating conditional guards simultaneously.
#
# In this notebook, we look at:
# 1. Simple Literal and Or Patterns
# 2. Sequence Unpacking and Matching (Lists and Tuples)
# 3. Mapping Extractor Patterns (Dictionaries)
# 4. Class Pattern Matching (Type and Attribute Inspection)
# 5. Conditional Guards and As-bindings

# %% [markdown]
# ## 1. Literal and Or Patterns
# Literal matches compare values directly. The Or pattern (`|`) allows matching multiple candidates in a single branch, and the wildcard (`_`) acts as the default fallback.

# %%
def respond_to_status(status_code):
    match status_code:
        case 200:
            return "OK"
        case 400 | 404:  # Or Pattern
            return "Client Error"
        case 500:
            return "Server Error"
        case _:  # Default fallback (Wildcard)
            return f"Unknown status: {status_code}"

print("Status 200:", respond_to_status(200))
print("Status 404:", respond_to_status(404))
print("Status 999:", respond_to_status(999))

# %% [markdown]
# ## 2. Sequence Patterns
# Match sequences (lists/tuples) based on their length, contents, or structures. You can bind specific items to variables or collect remainder items using the star operator (`*`).

# %%
def process_command(command_parts):
    match command_parts:
        case ["quit"]:
            print("System shutting down...")
        case ["make", filename]:  # Matches a list of length 2 starting with "make"
            print(f"Creating file: {filename}")
        case ["move", src, dest]:  # Matches a list of length 3 starting with "move"
            print(f"Moving {src} to {dest}")
        case ["delete", *files]:  # Matches "delete" followed by any number of files (unpacked)
            print(f"Deleting files: {files}")
        case _:
            print(f"Command not recognized: {command_parts}")

process_command(["make", "index.html"])
process_command(["delete", "style.css", "script.js", "logo.png"])
process_command(["invalid_command"])

# %% [markdown]
# ## 3. Mapping Patterns
# Mapping matching extracts values from dictionaries. Unlike sequence matching, a mapping pattern matches if the keys exist (extra keys in the dictionary are simply ignored).

# %%
def route_event(event):
    match event:
        case {"type": "click", "position": (x, y)}:  # Nested matching
            print(f"Click registered at coordinates: X={x}, Y={y}")
        case {"type": "keypress", "key": key_name}:
            print(f"Key pressed: {key_name}")
        case {"type": "hover"}:
            print("Hover event detected.")
        case _:
            print("Unknown event format.")

route_event({"type": "click", "position": (150, 300), "timestamp": 1294819})  # Extra keys ignored
route_event({"type": "keypress", "key": "Enter"})

# %% [markdown]
# ## 4. Class Pattern Matching
# Class patterns inspect the type of an object and extract attributes. Attributes can be matched positionally (if the class defines `__match_args__`) or explicitly by keyword.

# %%
class Point2D:
    # Explicitly defines positional matching order for match-case syntax
    __match_args__ = ("x", "y")
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

def inspect_geometry(geom):
    match geom:
        case Point2D(0, 0):  # Matches a Point2D at origin (positional)
            print("Point is at the origin.")
        case Point2D(x, 0):  # Matches a Point2D on X-axis (positional)
            print(f"Point is on the X-axis at X={x}")
        case Point2D(x=10, y=y_val):  # Matches Point2D where x is exactly 10 (keyword)
            print(f"Point on vertical line X=10, Y={y_val}")
        case Point2D(x, y):
            print(f"Generic Point2D: ({x}, {y})")
        case _:
            print("Not a Point2D geometry.")

inspect_geometry(Point2D(0, 0))
inspect_geometry(Point2D(5, 0))
inspect_geometry(Point2D(10, 25))

# %% [markdown]
# ## 5. Guards and As-bindings
# - **Guards (`if ...`)**: Allow adding arbitrary conditional checks directly inside the case branch.
# - **As-bindings (`pattern as name`)**: Bind the matched sub-pattern structure to a variable name for reference.

# %%
def analyze_user(user_data):
    match user_data:
        # Guard clause: only match admins with active status
        case {"role": "admin", "status": status} if status == "active":
            print("Access granted to administrator panel.")
        # Guard clause: deny access if user is suspended
        case {"status": "suspended"}:
            print("Access denied. Account is suspended.")
        # As-binding: binds the nested coordinates to 'coords'
        case {"type": "admin_click", "position": (int(), int()) as coords}:
            print(f"Admin click confirmed at position: {coords}")
        case _:
            print("Standard user access.")

analyze_user({"role": "admin", "status": "active"})
analyze_user({"role": "admin", "status": "suspended"})
analyze_user({"type": "admin_click", "position": (200, 450)})
