# %% [markdown]
# # Tutorial 11: SQL Scripting & Relational Databases (sqlite3)
#
# Python comes shipped with a complete relational database engine called `sqlite3`.
# In this notebook, we look at:
# 1. Thread-safe transactions and Parameterized Queries (combating SQL injection)
# 2. Custom Row Mapping Factories (returning dictionaries/structures instead of tuples)
# 3. Dynamic SQL Extensions (registering custom Python functions inside SQL statements)
# 4. Memory-Only Databases (`:memory:`)

# %%
import sqlite3

# %% [markdown]
# ## 1. In-Memory Database & Parameterized Queries
# Rather than reading and writing database files, we can instantiate an extremely fast database entirely in system RAM using `:memory:`.
#
# **CRITICAL EXPERT TIP:** Never format variables directly inside an SQL string (e.g. `f"SELECT * FROM users WHERE name = '{name}'"`). This makes the application vulnerable to **SQL Injection** attacks. Always use parameterized statements (`?` placeholder).

# %%
# 1. Establish an in-memory SQL session
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# 2. Create a table
cursor.execute("""
    CREATE TABLE members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        joined_year INTEGER
    )
""")

# 3. Parameterized insertions (safely escaping input)
members_data = [
    ("Alice", "Admin", 2024),
    ("Bob", "User", 2025),
    ("Charlie", "User", 2023)
]
cursor.executemany("INSERT INTO members (name, role, joined_year) VALUES (?, ?, ?)", members_data)
conn.commit()

# 4. Safely query the database using parameters
search_role = "User"
cursor.execute("SELECT * FROM members WHERE role = ?", (search_role,))
print("Query matches:")
for row in cursor.fetchall():
    print(row)

# %% [markdown]
# ## 2. Transaction Control
# When performing multiple dependent updates, we must wrap operations in a transaction. If any update fails, the entire transaction should rollback to keep the database consistent.
#
# Python's `connection` object acts as a context manager that automatically commits on success, and rolls back if an exception occurs.

# %%
print("--- Transaction rollback demonstration ---")
try:
    with conn:  # Context manager manages transaction (commit/rollback)
        # Valid update
        conn.execute("UPDATE members SET joined_year = 2026 WHERE name = 'Bob'")
        
        # Invalid update (triggering error)
        # Column 'non_existent_column' does not exist
        conn.execute("UPDATE members SET non_existent_column = 0 WHERE name = 'Alice'")
except sqlite3.OperationalError as e:
    print("Caught database operation error:", e)

# Verify 'Bob' was NOT permanently updated because the entire transaction rolled back!
cursor.execute("SELECT joined_year FROM members WHERE name = 'Bob'")
print("Bob's joined year after rollback (should remain 2025):", cursor.fetchone()[0])

# %% [markdown]
# ## 3. Custom Row Factories
# By default, sqlite3 queries return raw tuples (`(1, 'Alice', 'Admin', 2024)`). This makes code brittle to schema additions.
# Setting `connection.row_factory = sqlite3.Row` transforms query responses into mapping objects that look like dictionaries but remain memory efficient.

# %%
# Enable row factory on connection
conn.row_factory = sqlite3.Row
row_cursor = conn.cursor()

row_cursor.execute("SELECT * FROM members WHERE name = 'Alice'")
alice_row = row_cursor.fetchone()

print("Row Factory Output:")
print("Type:", type(alice_row))
print("Access by index: ID =", alice_row[0])
print("Access by column name: Name =", alice_row["name"])
print("Access keys:", alice_row.keys())

# %% [markdown]
# ## 4. Custom SQL Functions
# An advanced feature of Python's sqlite3 driver is the ability to register Python functions and execute them directly inside SQL queries.
# Use `connection.create_function(name, num_params, python_callable)`.

# %%
# Let's register a function that checks if a year is a leap year
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# Register custom function (name in SQL, number of args, Python callable)
conn.create_function("IS_LEAP_YEAR", 1, is_leap_year)

# Query database utilizing the custom SQL function!
extended_cursor = conn.cursor()
extended_cursor.execute("""
    SELECT name, joined_year, IS_LEAP_YEAR(joined_year) AS joined_on_leap
    FROM members
""")

print("Custom SQL function output:")
for row in extended_cursor.fetchall():
    print(f"Name: {row['name']}, Year: {row['joined_year']}, Joined Leap Year? {bool(row['joined_on_leap'])}")

# Close the database session
conn.close()
