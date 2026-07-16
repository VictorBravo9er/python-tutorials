# %% [markdown]
# # Tutorial 07: Pathlib, Tempfile & Logging Modules
#
# Writing production-ready scripts requires clean file system interaction and dynamic, structured logging.
#
# In this notebook, we look at:
# 1. Object-Oriented Paths with `pathlib`
# 2. Secure Temporary Files and Folders with `tempfile`
# 3. Enterprise-grade Structured `logging`

# %%
import logging
from pathlib import Path
import tempfile

# %% [markdown]
# ## 1. Pathlib: Modern Path Manipulation
# Pathlib replaces the legacy `os.path` module with an object-oriented path system.
#
# ### Advanced Pathlib Features:
# - Recursive directory search (`rglob`).
# - Modifying path segments (`with_name`, `with_suffix`).
# - Direct read/write utility methods (`read_text()`, `write_text()`).

# %%
# Getting paths
current_dir = Path.cwd()
print("Current Directory object:", current_dir)

# Constructing paths (using the division operator '/')
new_file = current_dir / "temp_notebook_asset.txt"
print("Joined path:", new_file)

# Direct writing & reading of files
new_file.write_text("Hello from Pathlib!")
print("File content read directly:", new_file.read_text())

# Renaming path suffix (in-memory path manipulation)
python_file = new_file.with_suffix(".py")
print("Suffix modified:", python_file)

# Check existence and properties
print("Exists?", new_file.exists())
print("Is File?", new_file.is_file())

# Clean up
new_file.unlink()

# Recursive search in current workspace (find all .py files in .src)
src_folder = Path(".src")
print("\nPython files inside .src:")
for py_path in src_folder.rglob("*.py"):
    # prints relative path to current directory
    print(f"- {py_path} (name: {py_path.name})")

# %% [markdown]
# ## 2. Tempfile: Secure Temporary Space
# Standard libraries often need temporary scratchpads. Creating files manually (e.g. `open('temp.txt')`) is prone to race conditions, security vulnerabilities, and left-over garbage files. `tempfile` guarantees security and auto-deletion.
#
# ### Key Utilities:
# - `TemporaryFile`: Anonymous temporary file (not visible in the directory listing).
# - `NamedTemporaryFile`: File visible in directory list (has a name).
# - `TemporaryDirectory`: Entire folder structure that is destroyed on context exit.

# %%
# NamedTemporaryFile example
print("--- Using NamedTemporaryFile ---")
with tempfile.NamedTemporaryFile(mode="w+t", suffix=".log") as temp_file:
    print("Temp file created at absolute path:", temp_file.name)
    temp_file.write("Scratchpad log entry 1\n")
    temp_file.seek(0)
    print("Content read:", temp_file.read().strip())
# File is automatically deleted here

# TemporaryDirectory example
print("\n--- Using TemporaryDirectory ---")
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    print("Temp directory created at:", temp_path)
    
    # Write multiple files inside the temp directory
    file1 = temp_path / "sub_file1.txt"
    file1.write_text("Hello inside temp dir")
    print(f"Created file: {file1} (content: '{file1.read_text()}')")
# Entire directory and its files are automatically destroyed here

# %% [markdown]
# ## 3. Logging: Structured Output
# Simple `print()` statements are insufficient for production systems. The `logging` module provides hierarchies, level controls, formatters, and handler routing.
#
# ### Advanced Logging Configuration:
# - Routing warnings/info to stdout, and errors to a dedicated file handler.
# - Setting custom formatters (injecting time, levels, and logger names).
# - Writing custom filters to drop specific logs.

# %%
# Define Logger
logger = logging.getLogger("AppLogger")
logger.setLevel(logging.DEBUG)  # Capture everything

# Avoid duplicate handler aggregation if cell re-run
if not logger.handlers:
    # 1. Console Handler (Logs INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 2. File Handler (Logs DEBUG and above)
    file_handler = logging.FileHandler("app_debug_output.log", mode="w")
    file_handler.setLevel(logging.DEBUG)
    
    # 3. Create Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 4. Add custom Filter to console (e.g., exclude logs containing word "SECRET")
    class NoSecretFilter(logging.Filter):
        def filter(self, record):
            return "SECRET" not in record.getMessage()
            
    console_handler.addFilter(NoSecretFilter())
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# Log messages
logger.debug("Starting initialization...")  # Goes only to file
logger.info("Application started successfully.")  # Goes to console and file
logger.warning("Low memory warning.")  # Goes to console and file
logger.info("This is a SECRET transaction record.")  # Drops from console due to filter, but goes to file

# Print file contents to show all logs
print("\n--- Dump of app_debug_output.log ---")
with open("app_debug_output.log", "r") as f:
    print(f.read().strip())

# Clean up log file
Path("app_debug_output.log").unlink()
