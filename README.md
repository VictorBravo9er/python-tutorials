# Python Advanced Features Tutorial (Categorized)

Welcome to the **Intermediate to Expert Python Advanced Features Tutorial**! This series is structured into logical subdirectories to help you master Python's robust built-in modules, advanced systems, metaprogramming constructs, and testing libraries.

---

## Directory & Tutorial Structure

### 📂 01_core_and_structures
Essential core syntax elements and built-in datatypes for intermediate/expert developers:
* **[00_guidelines.ipynb](file:///home/victor/tutorials/python/01_core_and_structures/00_guidelines.ipynb)**: Structural development guides and code quality practices.
* **[01_pattern_matching.ipynb](file:///home/victor/tutorials/python/01_core_and_structures/01_pattern_matching.ipynb)**: Structural Pattern Matching (`match-case`), literal/sequence/mapping matches, class extractor patterns, as-bindings, and conditional guards.
* **[02_collections.ipynb](file:///home/victor/tutorials/python/01_core_and_structures/02_collections.ipynb)**: Custom containers (`Counter`, `defaultdict`, `deque`, `NamedTuple`, `ChainMap`, `OrderedDict`).
* **[03_itertools.ipynb](file:///home/victor/tutorials/python/01_core_and_structures/03_itertools.ipynb)**: Stream-based iterator controls, infinite looping generators, sequence grouping/terminating, and combinatorics.
* **[04_functools_operator.ipynb](file:///home/victor/tutorials/python/01_core_and_structures/04_functools_operator.ipynb)**: Function metadata wrapping (`@wraps`), caching/memoization (`@lru_cache`, `@cache`), generic dispatching (`@singledispatch`), and high-performance selector operators.
* **[05_contextlib_dataclasses.ipynb](file:///home/victor/tutorials/python/01_core_and_structures/05_contextlib_dataclasses.ipynb)**: Custom context managers, `ExitStack` dynamic resource bindings, and structured data classes (`default_factory`, `__post_init__`, freezing).

### 📂 02_concurrency_and_async
Parallel programming and asynchronous event loops:
* **[06_concurrency.ipynb](file:///home/victor/tutorials/python/02_concurrency_and_async/06_concurrency.ipynb)**: Multithreading vs. Multiprocessing comparison, resource locks, safe queues, and GIL bypass strategies.
* **[07_advanced_asyncio.ipynb](file:///home/victor/tutorials/python/02_concurrency_and_async/07_advanced_asyncio.ipynb)**: Event loop control, structured concurrency (`TaskGroup` error handling), worker queue task distribution (`asyncio.Queue`), and synchronization events/locks.

### 📂 03_systems_and_io
Filesystem control, command line scripting, and database storage:
* **[08_pathlib_logging.ipynb](file:///home/victor/tutorials/python/03_systems_and_io/08_pathlib_logging.ipynb)**: OO path operations (`pathlib.Path`), secure temporary file setups (`tempfile`), and structured logging configurations.
* **[09_cli_subprocess.ipynb](file:///home/victor/tutorials/python/03_systems_and_io/09_cli_subprocess.ipynb)**: Command line parsers (`argparse` subparsers) and safe external subprogram executions (`subprocess`).
* **[10_sqlite3.ipynb](file:///home/victor/tutorials/python/03_systems_and_io/10_sqlite3.ipynb)**: Relational SQL operations, transaction commit/rollback parameters, row mapping factories, and memory databases.

### 📂 04_advanced_concepts
Type safety, class blueprints, and testing:
* **[11_typing_re.ipynb](file:///home/victor/tutorials/python/04_advanced_concepts/11_typing_re.ipynb)**: Advanced static typing interfaces (`Protocol`, generics, `TypeGuard`, `ParamSpec`) and complex regular expressions (lookarounds, named groups, verbose mode).
* **[12_metaprogramming_internals.ipynb](file:///home/victor/tutorials/python/04_advanced_concepts/12_metaprogramming_internals.ipynb)**: Python internals: custom descriptors (`__get__`/`__set__`), class creation hooking (`__init_subclass__`), metaclasses, and custom ABC mappings.
* **[13_testing_mocking.ipynb](file:///home/victor/tutorials/python/04_advanced_concepts/13_testing_mocking.ipynb)**: Mocks (`Mock`, `MagicMock`), dynamic mock patching (`unittest.mock.patch`), shared fixtures (`pytest.fixture`), and parameterized unit tests.

---

## Setup & Running the Notebooks

This project uses `uv` for lightning-fast virtual environment and package management.

### Prerequisites

Make sure you have `uv` installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation & Run

1. Navigate to the directory:
   ```bash
   cd /home/victor/tutorials/python
   ```

2. Start the Jupyter server automatically:
   ```bash
   uv run jupyter notebook
   ```
   *Note: `uv run` will automatically create a `.venv` (if not already present), download Python, install required libraries (`jupytext`, `jupyter`, `pytest`), and start the Jupyter environment.*

---

## How it works (Jupytext Format)
For version control and clean code tracking, the source scripts are developed as standard Python `.py` files inside the hidden `.src/` subdirectories in **Jupytext Percent format** and converted to Jupyter Notebooks (`.ipynb`) inside the target root folders.

If you edit any of the source `.py` files, convert them to notebooks by running:
```bash
for d in 01_core_and_structures 02_concurrency_and_async 03_systems_and_io 04_advanced_concepts; do
    for f in .src/$d/*.py; do
        uv run jupytext --to notebook --output "$d/$(basename "${f%.py}.ipynb")" "$f"
    done
done
```
