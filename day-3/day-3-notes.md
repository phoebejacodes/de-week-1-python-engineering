# Week 1

## Day 3: Logging and File Organization
**Theme:** "My code tells me what it's doing"

### Why Logging Exists
Logging is the practice of recording what a program is doing while it runs.  
Unlike `print()`, logs are structured, configurable, and designed for long-running or production systems.

Logging helps you:
- Understand program flow after execution
- Diagnose failures without rerunning code
- Monitor pipelines without manual inspection
- Reduce debugging and maintenance time

In production-quality code, **logging replaces print statements**.

---

### The Python Logging Module
Python includes a built-in `logging` module—no external libraries required.

A logger records events at different severity levels:

- `DEBUG` – detailed internal information for developers
- `INFO` – normal progress and high-level events
- `WARNING` – something unexpected but recoverable
- `ERROR` – a failure that prevented part of the program from working
- `CRITICAL` – a severe failure that may stop the program

By default, Python only displays `WARNING` and above unless configured.

---

### Basic Configuration (`logging.basicConfig`)
Logging behavior is controlled through configuration.

The most important configuration options:
- `level` – minimum severity level to record
- `format` – how each log message is displayed
- `datefmt` – timestamp formatting

Example:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"

### Important rule:

- basicConfig() must be called before any logging statements, or it will not apply.

## Formatting Log Output

Formatting makes logs readable and useful.

*Common formatting fields:*

 - %(asctime)s – when the event occurred

 - %(levelname)s – severity level

 - %(name)s – logger name

 - %(message)s – log message

 Example output:
 2025-07-22 09:26:00 - ERROR - City not found: Atlantis

 
### Logging in Data Pipelines

Logging answers critical operational questions:

1. Which step failed?

2. How many records were processed successfully?

3. Was a failure temporary or permanent?

4. Did retries occur?

A well-logged pipeline can be understood without rerunning it.

*Print vs Logging (Mental Model)*

print() is for quick local debugging

logging is for system observability

Print statements are temporary.
Logs are part of the system’s design.

### File Organization with pathlib
### Why `pathlib` Exists
`pathlib` provides an object-oriented way to work with file and directory paths.  
It replaces fragile, string-based path handling and unifies functionality that used to be spread across `os`, `glob`, and `shutil` :contentReference[oaicite:0]{index=0}.

Key benefit:
> Paths become objects with behavior, not just strings.

---

### Core Concepts
- `Path` is the main class used for file and directory paths
- Paths are **platform-independent** (Windows vs macOS/Linux handled automatically)
- Most file operations can be done directly on `Path` objects

Common imports:
```python
from pathlib import Path

#### Creating Paths

Common ways to create paths:

Path.cwd() → current working directory

Path.home() → user home directory

Path("some/file.txt") → from string

Path("folder") / "file.txt" → join paths (preferred)

The / operator joins paths cleanly without worrying about separators.

#### Inspecting Paths

Useful Path properties:

.name → filename

.stem → filename without extension

.suffix → file extension

.parent → containing directory

 * Paths can be chained: *
Path(__file__).parent

#### Reading and Writing Files

pathlib provides built-in methods for file I/O:

.read_text() / .read_bytes()

.write_text() / .write_bytes()

These methods:

automatically open and close files

reduce boilerplate

make intent explicit

Example:
content = Path("data.txt").read_text()
Path("output.txt").write_text(content)

#### Why This Matters for Pipelines

Using pathlib:

makes code portable across machines

avoids hardcoded paths

improves readability and maintainability

supports organized project structures

Rule of thumb:

If paths matter to your pipeline, they should be first-class objects.


