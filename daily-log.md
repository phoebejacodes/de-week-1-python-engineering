# Week 1 Daily Log

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

## Day 2
- Start time: 6:47 AM
- End time: 8:21 PM
- Hours Worked: ~8 hours
-###Completed:
- [x]Explored common failure modes in API calls (404s, connection errors, missing keys)
- [x]Differentiated HTTP errors vs runtime/transport exceptions
- [x]Implemented try/except patterns for controlled failure handling
- [x]Used raise_for_status() to convert HTTP errors into exceptions
- [x]Built safe API wrapper functions with timeouts
- [x]Practiced handling multiple exception types
- [x]Introduced environment variables for configuration
- [x]Managed API keys securely (no hardcoding)
- [x]Used .env files with python-dotenv
- [x]Implemented retries with capped attempts
- [x]Added rate limiting via request delays
- [x]Built a multi-step, resilient ingestion pipeline
- [x]Produced summary reporting for pipeline outcomes
- [x]Practiced bash environment variables and shell configuration

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

### Tomorrow's focus:
- Observability: making pipelines self-describing through structured logging instead of print statements
-Maintainability: organizing files, paths, and project structure for long-term scalability
-More Bash logic (variables, loops, conditionals) to support repeatable workflows

- Struggled with:
- Key learnings:
- Tomorrow's focus: