# Day 4 – Command Line Interfaces (CLI)

## Theme  
**“My scripts accept instructions from the outside.”**

---

## Why This Matters

So far, scripts have required editing the code itself to change behavior.  
Command Line Interfaces (CLIs) allow programs to:

- Accept input dynamically
- Be reused without modification
- Integrate into automation pipelines
- Be run by other programs or schedulers

CLIs are how real tools communicate with users and other programs.
---

## What Is a CLI?

A **Command Line Interface** allows a program to receive input from the terminal.

Example:
```bash
python script.py --city London --units metric

Instead of hardcoding values, behavior is controlled by arguments passed at runtime.

``` 
## sys.argv – The Basics

sys.argv is a list that contains command-line arguments.
``` python
import sys
print(sys.argv)
 

Example:
``` python 
script.py hello world
 

Produces:

['script.py', 'hello', 'world']
``` 

sys.argv[0] → script name

sys.argv[1:] → user inputs

Useful for simple scripts, but not ideal for complex tools.

- Hard to manage
- No built-in validation
- Easy to break

Good for learning, not ideal for production.

## Why argparse Is Better

The argparse module is the standard way to build professional CLIs.

### It provides:
- Automatic help messages
- Type validation
- Clear error handling
- Named arguments and flags

### Using argparse allows you to:
- Build reusable tools
- Avoid hardcoding values
- Support automation and scheduling
- Match professional software practices

Example:
``` python 

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--city", required=True)
parser.add_argument("--units", default="metric")

args = parser.parse_args()
Run it like:

bash
Copy code
python weather.py --city London --units metric
``` 

## Positional vs Optional Arguments

- Positional arguments
Required values (e.g., filenames)

- Optional arguments
Flags that modify behavior (e.g. --verbose, --output)

Example:
``` python 
parser.add_argument("input_file")
parser.add_argument("--limit", type=int, default=10)
``` 

## Why This Matters in Real Projects

CLI tools allow:

- Automation via scripts or schedulers
- Clean separation between logic and configuration
- Reusability across environments
- Integration into data pipelines

This is how production tools are built and deployed.

## Key Takeaway

Scripts run once.
CLI tools scale.

Learning CLI design means not just writing code — building usable software.
