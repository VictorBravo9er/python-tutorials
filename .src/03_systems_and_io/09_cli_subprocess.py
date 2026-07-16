# %% [markdown]
# # Tutorial 10: CLI Development & Subprocess Control
#
# Writing developer tools requires robust user input parsing and safe coordination with external system tools.
# In this notebook, we look at:
# 1. Professional Command-Line Interfaces with `argparse` (including subcommands)
# 2. Executing external programs safely with `subprocess` (handling pipes, streams, and timeouts)

# %%
import argparse
import subprocess
import sys

# %% [markdown]
# ## 1. CLI Development with argparse
# `argparse` is a built-in module designed to parse command-line arguments. It automatically creates clear `--help` outputs and handles conversions.
#
# ### Advanced Argparse Features:
# - **Subparsers:** Creating commands like `docker run` or `git commit`, where each subcommand has its own specific set of options.
# - **Type Checking & Choices:** Ensuring arguments match dynamic constraints directly at the boundary.

# %%
def setup_cli_parser():
    # 1. Setup root parser
    parser = argparse.ArgumentParser(
        prog="assetmgr",
        description="A professional asset manager CLI."
    )
    
    # 2. Setup subparsers for commands (e.g. 'add' vs 'delete')
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available sub-commands")
    
    # Subcommand: add
    add_parser = subparsers.add_parser("add", help="Add a new asset")
    add_parser.add_argument("name", type=str, help="Asset identifier name")
    add_parser.add_argument(
        "--type", 
        choices=["image", "audio", "video"], 
        default="image", 
        help="Type classification of the asset (default: %(default)s)"
    )
    add_parser.add_argument("--size", type=int, required=True, help="Asset size in bytes")
    
    # Subcommand: list
    list_parser = subparsers.add_parser("list", help="List all assets")
    list_parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")
    
    return parser

# Testing the parser programmatically (by simulating command-line arguments)
parser = setup_cli_parser()

print("--- Simulated CLI Call: assetmgr add logo.png --size 1024 ---")
args1 = parser.parse_args(["add", "logo.png", "--size", "1024"])
print(f"Parsed Command: {args1.command}, Name: {args1.name}, Type: {args1.type}, Size: {args1.size} bytes")

print("\n--- Simulated CLI Call: assetmgr list --format json ---")
args2 = parser.parse_args(["list", "--format", "json"])
print(f"Parsed Command: {args2.command}, Format: {args2.format}")

# %% [markdown]
# ## 2. Safe Subprocess Management
# Python's `subprocess` module allows spawning new processes, connecting to their input/output/error pipes, and obtaining their return codes.
#
# ### Expert Guidelines:
# - **Avoid `shell=True`:** Passing string commands with `shell=True` makes code highly vulnerable to Shell Injection attacks. Always pass arguments as a list of strings (`['ls', '-l']`).
# - **Always Set `timeout`:** External calls can hang indefinitely. Setting a timeout prevents scripts from freezing.
# - **Use `capture_output=True` & `text=True`:** Captures stdout/stderr directly as python string objects instead of byte arrays.

# %%
# 1. Simple command execution
print("--- Simple Subprocess Call ---")
result = subprocess.run(["echo", "Hello from subprocess!"], capture_output=True, text=True, check=True)
print("Stdout:", result.stdout.strip())
print("Return Code:", result.returncode)


# 2. Handling errors and timeouts
print("\n--- Error Handling and Timeout Checks ---")
try:
    # Simulating a slow command that exceeds the timeout
    # 'sleep 10' will raise TimeoutExpired because we set a 1-second limit
    subprocess.run(["sleep", "10"], timeout=1)
except subprocess.TimeoutExpired as e:
    print("Caught expected timeout exception:", e)

try:
    # Executing a command that returns a non-zero exit status
    subprocess.run(["ls", "non_existent_directory_abc"], capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print("Caught expected process execution error:")
    print("  Command failed:", e.cmd)
    print("  Exit status code:", e.returncode)
    print("  Stderr output:", e.stderr.strip())


# 3. Piping outputs from one process to another (e.g. cat | grep)
print("\n--- Pipeline Emulation ---")
# Let's search for "admin" within a list of users
users_data = "alice:user\nbob:admin\ncharlie:user\n"

# Start the first command (echo users_data)
p1 = subprocess.Popen(["echo", users_data], stdout=subprocess.PIPE, text=True)
# Start the second command (grep admin), linking its stdin to p1's stdout
p2 = subprocess.Popen(["grep", "admin"], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)

# Allow p1 to receive SIGPIPE if p2 exits
p1.stdout.close()

# Wait for pipeline completion and get output
output, _ = p2.communicate()
print("Pipeline Result:")
print(output.strip())
