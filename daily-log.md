# Week 1 Daily Log
---

## Day 1
- Start time: 6:54 AM
- End time: 7:45 PM
- Hours Worked: ~ 11 hours
- ### Completed:
- [x] First API call with requests
- [x] JSON parsing
- [x] Nested JSON access
- [x] Query parameters
- [x] Writing to JSON files
- [x] Writing to CSV files
- [x] Combined pipeline script
- [x] Bash navigation basics
- [x] First Bash script
- [x] Exercise: todos with users

### Struggled with:
- Translating API documentation into Python logic
- Avoiding refetching the same data repeatedly 
- Thinking through data shape before writing code
- Bash quirks

### Key learnings:
- response.json() converts to Python dict
- with open() is the proper way to handle files
- response.json() converts API responses into Python lists and dictionaries
- API endpoints determine data shape (/resource vs /resource/{id})
- Nested JSON is accessed by chaining keys
- CSV requires an explicit schema; JSON preserves structure
- Event/task data (todos) can be large and must be handled carefully
- Bash is a powerful tool for validating outputs, not just navigation
- wc -l counts lines, not records — format matters
- Different data formats require different inspection tools (grep vs jq)
- The Fetch → Transform → Persist pattern is reusable across all pipelines
---

## Day 2
- Start time: 6:47 AM
- End time: 8:21 PM
- Hours Worked: ~8 hours

- ### Completed:
- [x] Explored common failure modes in API calls (404s, connection errors, missing keys)
- [x] Differentiated HTTP errors vs runtime/transport exceptions
- [x] Implemented try/except patterns for controlled failure handling
- [x] Used raise_for_status() to convert HTTP errors into exceptions
- [x] Built safe API wrapper functions with timeouts
- [x] Practiced handling multiple exception types
- [x] Introduced environment variables for configuration
- [x] Managed API keys securely (no hardcoding)
- [x] Used .env files with python-dotenv
- [x] Implemented retries with capped attempts
- [x] Added rate limiting via request delays
- [x] Built a multi-step, resilient ingestion pipeline
- [x] Produced summary reporting for pipeline outcomes
- [x] Practiced bash environment variables and shell configuration

### Struggled with:
-Reasoning about when retries are appropriate vs wasteful
-Coordinating Python environments and installed packages
-Translating conceptual retry logic into clean control flow
-Debugging path and interpreter mismatches across tools
-Remembering when shell behavior differs from program behavior

### Key learnings:
-HTTP status codes indicate application-layer outcomes; exceptions signal system-level failures
-try/except/else/finally structures control execution flow under failure
-raise_for_status() simplifies error handling by separating success and failure paths
-Environment variables are the correct way to manage secrets and configuration
-.env files enable local development without leaking credentials
-Programs inherit environment variables from the shell at runtime
-Retries should be reserved for transient infrastructure failures, not bad data
-Rate limiting is an essential part of responsible API consumption
-Pipelines should continue operating despite partial failures
-Summary reporting is as important as raw data ingestion
-Tooling noise (VS Code, Python env discovery) is normal and not a signal of broken code
-Robust pipelines are defined by how they fail, not how they succeed

---

## Day 3 (Christmas :christmas_tree: )
- Start time: 7:18 AM
- End time: 7:01 PM
- Hours Worked: ~8 hours
- ### Completed:
- [x] Implemented structured logging using Python’s `logging` module  
- [x] Learned the difference between `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`  
- [x] Replaced `print()` statements with proper logging calls  
- [x] Configured logging to output to both console and file  
- [x] Learned when and why to use `basicConfig()` vs custom log handlers  
- [x] Built a reusable logging setup across scripts  
- [x] Refactored scripts into a clean, production-style pipeline  
- [x] Introduced `pathlib` for clean, OS-agnostic file handling  
- [x] Organized project structure into:
  - `src/`
  - `data/`
  - `logs/`
  - `output/`
- [x] Built a fully structured pipeline with:
  - Config management
  - API ingestion
  - Error handling
  - Logging
  - Output persistence
- [x] Created a Bash runner to automate execution  
- [x] Used environment variables for secrets (`.env`)
- [x] Learned how logging enables observability and debugging in real systems  

### Struggled with:
- Structuring a real project instead of a single script  
- Managing relative paths across folders  
- Keeping configuration separate from code  
- Thinking in terms of pipelines instead of scripts 

### Key Laernings:
- Logging is for **humans and systems**, not just debugging  
- `logging` provides visibility into runtime behavior and failures  
- Log levels communicate intent and severity  
- `print()` is for exploration; logging is for production  
- `pathlib` makes filesystem code safer and cleaner  
- Separating config, logic, and execution improves maintainability  
- Structured projects scale better than scripts  
- Good pipelines fail loudly and clearly  
---

## Day 4
- Start time: 9:31 AM
- End time: 7:18 PM
- Hours Worked: ~ 9 hours

### Completed

- [x] Basic argparse setup with positional and optional arguments
- [x] Argument types, validation, and choices
- [x] Short flags (-v) and long flags (--verbose)
- [x] Mutually exclusive argument groups
- [x] Built weather CLI tool with multiple options
- [x] File input via CLI (--file flag)
- [x] Subcommands pattern (fetch, convert, info)
- [x] Environment variable fallbacks in CLI
- [x] Bash functions (parameters, return values, local variables)
- [x] Bash argument parsing with case statements
- [x] Shell script to run Python CLI with logging
- [x] Combined everything into pipeline CLI tool

### Struggled With
- Understanding how `argparse` wires together subcommands and arguments
- Knowing where logic should live (main function vs handler functions)
- Keeping track of how arguments flow from CLI → parser → function
- Remembering when to use positional vs optional arguments
- Debugging silent failures caused by incorrect file paths or missing flags
- Understanding how scripts, shell commands, and Python execution interact
- Hardest day so far — complexity ramped up fast
- Code structure feels jumbled, hard to follow the ordering
- Relied heavily on AI to complete exercises
- Understanding is general, not deep
- Feeling intimidated by not being able to do it alone

### Key Learnings
- CLI tools are just structured Python programs with argument parsing
- `argparse` turns raw user input into structured data
- `subparsers` let you design multi-command tools (like `git`, `docker`)
- Environment variables are essential for secrets and configuration
- Logging replaces print statements in real applications
- Separating logic (fetch, convert, output) makes programs scalable
- File paths should always be handled with `pathlib`
- Debugging CLI tools requires reading error output carefully
- You don’t need to memorize — you need to understand patterns

### Honest State
- Confidence: Shaky, proud of myself
- Understanding: Surface level, building
- Determination: Choosing to push forward
- Trust in process: Holding on

### Code Patterns to Remember
```python
# Mutually exclusive arguments
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--cities", "-c")
group.add_argument("--file", "-f")
```
```python
# Subcommand with handler
subparsers = parser.add_subparsers(dest="command")
fetch_parser = subparsers.add_parser("fetch")
fetch_parser.set_defaults(func=cmd_fetch)
```
```bash
# Bash argument parsing
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file) FILE="$2"; shift 2 ;;
        -v|--verbose) VERBOSE=true; shift ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done
```
```python
# ========== SECTION 1: IMPORTS ==========
# "What tools do I need?"
import argparse          # For CLI arguments
import requests          # For API calls
import json              # For JSON files
import logging           # For logging
from pathlib import Path # For file paths
from dotenv import load_dotenv  # For .env files
import os                # For environment variables

# ========== SECTION 2: SETUP/CONSTANTS/CONFIG ==========
# "What needs to happen before anything else?"
load_dotenv()  # Load .env file
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ========== SECTION 3: HELPER FUNCTIONS ==========
# "Small, single-purpose functions"

def setup_logging(verbose):
    """Just sets up logging. Nothing else."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level)
    return logging.getLogger(__name__)

def fetch_weather(city, api_key):
    """Just fetches weather. Nothing else."""
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": api_key, "units": "metric"}
    )
    return response.json()

def save_to_file(data, path):
    """Just saves data. Nothing else."""
    Path(path).write_text(json.dumps(data, indent=2))

# ========== SECTION 4: MAIN FUNCTION ==========
# "Combines helpers to do the actual work"

def main():
    # Step 1: Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("cities")
    parser.add_argument("--output", default="weather.json")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    
    # Step 2: Setup
    logger = setup_logging(args.verbose)
    
    # Step 3: Do the work
    cities = args.cities.split(",")
    results = []
    for city in cities:
        weather = fetch_weather(city, API_KEY)
        results.append(weather)
    
    # Step 4: Save results
    save_to_file(results, args.output)

# ========== SECTION 5: ENTRY POINT ==========
# "This is where Python starts running"

if __name__ == "__main__":
    main()

```
---
## Day 5
- Start time: 8:02 AM
- End time: 6:19 PM
- Hours Worked: ~ 8 hours


### Completed

- [x] Learned how failures actually occur in real systems (timeouts, 5xx errors, rate limits)
- [x] Implemented retry logic with fixed delays
- [x] Implemented exponential backoff for safer retries
- [x] Learned why naive retries can *make outages worse*
- [x] Built a reusable retry helper with logging and retry limits
- [x] Implemented rate limiting to prevent API abuse
- [x] Learned how to space requests intentionally over time
- [x] Built a resilient request pipeline combining:
  - rate limiting  
  - retries  
  - backoff  
  - logging  
- [x] Implemented a full **Circuit Breaker** pattern
- [x] Understood CLOSED → OPEN → HALF-OPEN transitions
- [x] Built a production-style resilient pipeline with:
  - stats tracking  
  - retry awareness  
  - graceful failure handling  
- [x] Learned how real systems protect themselves under load
- [x] Connected all previous concepts into a single architecture

---

###  Struggled With

- Understanding *why* each resilience layer exists and when it should trigger  
- Keeping mental separation between:
  - retry logic  
  - rate limiting  
  - circuit breaking  
- Feeling overwhelmed by how many moving parts are involved  
- Realizing how fragile naive code actually is  
- Understanding when retries help vs when they make things worse  
- Tracking state across attempts (failures, successes, cooldowns)
- Recognizing that production systems **expect** failure constantly  

---

### Key Learnings

- Failures are not edge cases — they are normal conditions  
- Retry ≠ reliability unless paired with backoff  
- Rate limiting protects both the API **and** your application  
- Circuit breakers prevent cascading failures  
- Resilience comes from **layers**, not single fixes  
- Observability (logs, metrics) is just as important as functionality  
- Production code is designed to *fail safely*, not perfectly  
- Writing robust systems requires defensive thinking, not optimism 

### Honest State
- Understanding: growing steadily  
- Overwhelm: high, but productive  
- Progress: undeniable  
- Direction: clear  

### Pattern to remember: 

**Mental Model**
┌──────────────────────────┐
│ 1. Command-Line Interface│  ← user input
├──────────────────────────┤
│ 2. Validation & Parsing  │  ← make input safe
├──────────────────────────┤
│ 3. Rate Limiting         │  ← don't overload APIs
├──────────────────────────┤
│ 4. Retry Logic           │  ← recover from temporary failures
├──────────────────────────┤
│ 5. Circuit Breaker       │  ← stop if system is unhealthy
├──────────────────────────┤
│ 6. Business Logic        │  ← fetch, process, save data
├──────────────────────────┤
│ 7. Logging & Metrics     │  ← observability
└──────────────────────────┘

| Layer           | Purpose           | Protects Against     |
| --------------- | ----------------- | -------------------- |
| CLI             | Input control     | Bad usage            |
| Validation      | Input correctness | Bad parameters       |
| Rate Limiting   | API overload      | Throttling / bans    |
| Retry Logic     | Transient failure | Timeouts / flakiness |
| Circuit Breaker | System failure    | Cascading outages    |
| Logging         | Observability     | Silent failures      |
| Output Handling | Persistence       | Data loss            |
---

## Day 6
- Start time: 9:07 AM
- End time: 6:49 PM
- Hours Worked: ~ 7 hours

### Completed
- Explored **CSV, JSON, and Parquet** formats in depth
- Built scripts to:
  - Read/write CSV, JSON, and JSONL
  - Compare file sizes and performance
  - Convert between formats using Pandas and PyArrow
- Learned how **Parquet** stores data column-wise and why it’s faster and smaller
- Implemented **format converters** (CSV ↔ JSON ↔ Parquet)
- Built tools to inspect file metadata (rows, columns, schema)
- Learned **chunked processing** for large datasets
- Implemented **retry logic**, **rate limiting**, and **circuit breakers**
- Built a full **resilient pipeline** with:
  - Logging
  - Retry + backoff
  - Error handling
  - Graceful failure
- Learned how to debug and fix environment issues (conda, pyarrow, path issues)

### Struggled With
- Debugging Python environment issues (conda + pyarrow + system libs)
- Distinguishing when to use:
  - retry vs retry-with-backoff  
  - rate limiting vs circuit breaker  
- Feeling overwhelmed by how many moving parts exist in a “real” pipeline
- Internalizing that most production code is defensive

### Key Learnings
- **CSV** is simple but inefficient; everything is a string
- **JSON** preserves structure but is large and slow for analytics
- **Parquet** is columnar, compressed, and designed for analytics workloads
- Chunking is mandatory for large files to avoid memory issues
- Real pipelines are built from small, composable parts
- Most complexity exists to handle *failure*, not success
- You don’t need to invent solutions — you assemble proven patterns
- Understanding > memorization; clarity > speed
---
## Day 7
- Start time: 8:40 AM
- End time: 1:25 PM
- Hours Worked: ~ 4 hours

### Completed
- Built a **fully modular data pipeline** combining:
  - CLI interface with subcommands
  - API ingestion with retry + rate limiting
  - Format conversion (CSV, JSON, JSONL, Parquet)
  - Robust file handling and schema awareness
- Implemented **end-to-end data flow**:
  - Input → Validation → Processing → Output
- Built and validated:
  - `config.py` for centralized configuration
  - `api.py` for resilient API access
  - `formats.py` for format conversion
  - `pipeline.py` for orchestration
  - CLI entrypoint with argparse
- Successfully handled:
  - Partial failures
  - Rate limiting
  - Logging
  - Structured output
- Debugged and resolved environment issues (conda, pyarrow, PATH conflicts)
- Verified full pipeline execution with real API data


### Struggled With
- Environment instability (conda + pyarrow conflicts)
- Understanding *why* certain abstractions existed before seeing them work together
- Debugging dependency issues that were unrelated to code logic
- Mental overload from managing many moving parts at once
- Distinguishing “code that works” vs “code that scales cleanly”


### Key Learnings
- Real-world data engineering is **systems design**, not just code
- Clean abstractions matter more than clever code
- Most complexity comes from *interfaces* between components
- Configuration, logging, and error handling are first-class features
- Once patterns repeat (retry, format handling, IO), everything becomes composable
- Understanding > memorization — the architecture finally “clicked”

---
---
## Week 1 Complete

### What I Built
- Day 1: API calls, JSON parsing, file I/O
- Day 2: Error handling, authentication, environment variables
- Day 3: Logging, project structure, pathlib
- Day 4: CLI tools with argparse, Bash scripting
- Day 5: Retry logic, rate limiting, circuit breakers
- Day 6: Multiple data formats, Parquet, format conversion
- Day 7: Complete integrated pipeline with all features

### Key Skills Gained
- Production-ready Python scripting
- Error handling patterns
- API integration with resilience
- Command-line tool development
- Multiple data formats
- Bash scripting basics
- Project organization
- Debugging environment and dependency issues

### What Was Hard
- Keeping the big picture in mind while managing many moving parts
- Understanding why certain abstractions (like config layers or helpers) exist
- Debugging environment issues (Python versions, packages, paths)
- Knowing when something was “good enough” versus overengineering
- Trusting myself when things felt confusing but were actually clicking

### What Clicked
- How all the pieces connect into a real pipeline
- Why separation of concerns matters
- How retries, rate limiting, and logging work together in production
- That complexity becomes manageable when broken into layers
- That I can reason through unfamiliar systems with enough patience


### Reflection
This week has been both challenging and deeply rewarding. It pushed me to think more deliberately about how systems are designed, not just how code is written. Concepts that once felt abstract like data flow, resilience and structure are now beginning to connect into a coherent mental model.

I’m gaining confidence in navigating complexity and more importantly, I’m developing the curiosity and discipline required to keep learning at depth. This experience has made it clear that building reliable software is as much about design and understanding as it is about writing code *and* I’m motivated to keep going.