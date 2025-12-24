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

### Tomorrow's focus:
- Error handling
- API authentication
- More Bash (pipes, grep):
- Struggled with:
- Key learnings:
- Tomorrow's focus: