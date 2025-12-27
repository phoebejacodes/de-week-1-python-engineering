## Day 5 — Retry Logic and Resilience
Theme: "My code survives when things fail"

### Overview
Today focuses on understanding how real-world systems fail and how to design code that can handle those failures gracefully. The goal is to move beyond “happy path” programming and build resilient, production-ready logic.

---

### Key Concepts 

#### 1. **Timeouts**
- Occurs when a request takes too long to receive a response.
- Common in slow networks or overloaded APIs.
- Handled using `timeout=` in requests.
- Prevents programs from hanging indefinitely.

Example:
```python
requests.get(url, timeout=2)
```

### 2. Connection Errors

Happen when a server cannot be reached (DNS issues, network failure, server offline).

Typically raised as requests.exceptions.ConnectionError.

Must be caught to prevent program crashes.

### 3. HTTP Errors

Different HTTP status codes indicate different failure types:

**404 – Resource not found**
**500 – Server error**
**429 – Rate limited (too many requests)**

These errors do not always raise exceptions automatically and must be checked explicitly.

### 4. Successful Requests

A **200** OK response indicates the request succeeded.

Valid responses should still be validated before use.

#### Key Insight

Errors are not exceptional—they are expected behavior in distributed systems. A resilient program is not one that never fails, but one that knows how to fail safely.

This understanding forms the foundation for building reliable APIs, data pipelines, and production systems.

#### Robust programs:

- Anticipate failures
- Handle them gracefully
- Continue operating when possible

### Reference Tables 

| Failure Type    | Meaning                     | Action      |
| --------------- | --------------------------- | ----------- |
| Timeout         | Server too slow             | Retry       |
| ConnectionError | Network/DNS issue           | Retry       |
| HTTPError       | Server responded with error | Log + retry |
| Success         | 200 OK                      | Return data |


| Failure Type     | Example                   | How To Handle It    |
| ---------------- | ------------------------- | ------------------- |
| Timeout          | API takes too long        | Retry with delay    |
| Connection error | No internet / DNS fail    | Catch + log         |
| HTTP 4xx         | Bad request, invalid city | Report & skip       |
| HTTP 5xx         | Server failure            | Retry then fail     |
| Invalid input    | Bad CLI args              | argparse validation |

#### Common Failure Types (What Can Go Wrong)

| Failure Type     | Example             | What It Means               | Typical Cause                   | **Action to Take**            |
| ---------------- | ------------------- | --------------------------- | ------------------------------- | ----------------------------- |
| Timeout          | Request hangs       | Server too slow to respond  | Network latency, overloaded API | Retry with timeout + backoff  |
| Connection Error | Cannot reach server | DNS or network failure      | Wrong URL, no internet          | Retry + log error             |
| HTTP 400–499     | Client error        | Bad request or auth         | Invalid params, expired API key | Fix request, validate input   |
| HTTP 401         | Unauthorized        | Invalid/missing credentials | Wrong or missing API key        | Refresh or set credentials    |
| HTTP 403         | Forbidden           | Access denied               | Missing permissions             | Check API plan or permissions |
| HTTP 404         | Not Found           | Resource doesn’t exist      | Wrong endpoint or ID            | Validate URL or input         |
| HTTP 429         | Too Many Requests   | Rate limit exceeded         | Too many API calls              | Backoff + retry later         |
| HTTP 5xx         | Server error        | API failure                 | Remote system problem           | Retry with backoff            |
| Invalid JSON     | Parse error         | Bad or partial response     | Corrupt data                    | Validate response             |
| File Not Found   | Missing file        | Wrong path                  | Bad configuration               | Check path / create file      |
| Permission Error | Access denied       | File permissions            | OS restrictions                 | Change permissions            |
| Missing Env Var  | Config missing      | Env not set                 | Deployment error                | Fail fast with message        |


#### Safeguards & How to Apply Them

| Safeguard             | Purpose                         | When to Use            | How to Implement                 |
| --------------------- | ------------------------------- | ---------------------- | -------------------------------- |
| `try / except`        | Prevent crashes                 | Any risky operation    | Wrap API, file, or parsing logic |
| Timeouts              | Avoid hanging forever           | Network requests       | `requests.get(..., timeout=10)`  |
| Retries               | Recover from temporary failures | APIs, DBs              | Loop with retry count            |
| Exponential Backoff   | Prevent overload                | APIs under rate limits | `sleep(2 ** attempt)`            |
| Jitter                | Prevent retry storms            | Distributed systems    | Randomize delay                  |
| Logging               | Visibility into failures        | Everywhere             | `logging.info/error()`           |
| Input Validation      | Catch bad input early           | CLI, user input        | `argparse`, type checks          |
| Defaults              | Safe fallback behavior          | Optional config        | Default values                   |
| Environment Variables | Secure configuration            | Secrets, keys          | `os.getenv()`                    |
| Exit Codes            | Signal failure to OS            | Scripts & automation   | `sys.exit(1)`                    |
| Structured Errors     | Easier debugging                | APIs, pipelines        | Consistent error messages        |


#### 1. Failure Types & What They Mean
| Failure Type     | Example                  | What It Means                  | Typical Cause             |
| ---------------- | ------------------------ | ------------------------------ | ------------------------- |
| Timeout          | Request hangs            | Server too slow or unreachable | Network latency, overload |
| Connection Error | DNS / connection failure | Host unreachable               | Bad URL, no internet      |
| HTTP 4xx         | 400–499                  | Client-side problem            | Bad request, auth failure |
| HTTP 5xx         | 500–599                  | Server-side failure            | Server crash, overload    |
| Rate Limit (429) | Too many requests        | API protection                 | Exceeded request quota    |
| Invalid Data     | KeyError, ValueError     | Unexpected response shape      | API change or bug         |
| Partial Failure  | Some requests fail       | Unstable upstream              | Need retries              |
| Complete Failure | All requests fail        | Outage                         | Circuit breaker triggers  |

#### 2. Failure Handling Techniques
| Technique           | Purpose                     | When to Use            |
| ------------------- | --------------------------- | ---------------------- |
| `try/except`        | Catch runtime errors        | Always                 |
| Retry logic         | Retry transient failures    | Network instability    |
| Exponential backoff | Reduce load during failures | Rate-limited APIs      |
| Timeout             | Prevent hanging requests    | All external calls     |
| Logging             | Visibility into behavior    | Debugging + monitoring |
| Graceful fallback   | Keep system running         | Partial outages        |
| Circuit breaker     | Prevent overload            | Repeated failures      |
| Rate limiting       | Avoid bans / throttling     | Public APIs            |

#### 3. Retry Strategy Breakdown
| Concept             | Description                         |
| ------------------- | ----------------------------------- |
| Fixed retry         | Retry every N seconds               |
| Exponential backoff | Delay doubles each retry            |
| Jitter              | Random delay to avoid sync storms   |
| Max retries         | Hard stop to prevent infinite loops |
| Retry on            | Timeout, 5xx, connection errors     |
| Do NOT retry        | 4xx errors (bad input)              |

#### 4. Retry vs Circuit Breaker
| Feature   | Retry                          | Circuit Breaker           |
| --------- | ------------------------------ | ------------------------- |
| Purpose   | Recover from temporary failure | Prevent repeated failures |
| Behavior  | Keeps retrying                 | Stops trying temporarily  |
| Used when | Failure is intermittent        | Failure is persistent     |
| Example   | Network hiccup                 | API completely down       |


#### 5. Logging Levels (Mental Model)
| Level    | Meaning                    | When to Use      |
| -------- | -------------------------- | ---------------- |
| DEBUG    | Detailed internal info     | Development      |
| INFO     | Normal operation           | High-level flow  |
| WARNING  | Unexpected but recoverable | Retry triggered  |
| ERROR    | Failed operation           | API failure      |
| CRITICAL | System unusable            | Shutdown / abort |

#### 6. CLI Design Patterns Used
| Concept                 | Purpose                         |
| ----------------------- | ------------------------------- |
| `argparse`              | User input via CLI              |
| Subcommands             | `fetch`, `convert`, `list`      |
| Mutually exclusive args | Prevent invalid input combos    |
| Flags (`--verbose`)     | Control behavior                |
| Defaults                | Sensible behavior without flags |

#### 7. Resilience Patterns Implemented
| Pattern            | Where Used  | Why                      |
| ------------------ | ----------- | ------------------------ |
| Retry with backoff | HTTP calls  | Prevent overload         |
| Rate limiting      | API calls   | Respect API limits       |
| Circuit breaker    | API outages | Avoid cascading failures |
| Logging            | Everywhere  | Debug + audit            |
| Input validation   | CLI args    | Fail fast                |
| Environment config | `.env`      | Secure secrets           |

### Data Pipeline (Mental Model)
┌─────────────────────┐
│  USER / SYSTEM INPUT │
│  (CLI Arguments)     │
│  - Cities            │
│  - Flags (--verbose) │
│  - Output format     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  CLI PARSER (argparse)
│  - Validates input
│  - Enforces rules
│  - Routes logic
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  CONFIG LAYER       │
│  - Env variables     │
│  - API keys          │
│  - File paths        │
│  - Logging setup     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  CORE PIPELINE LOGIC│
│  (Your Business Logic)
│                     │
│  ┌─────────────────┐│
│  │ Fetch Data       │◄─── API (HTTP)
│  │ Retry + Backoff  │
│  └─────────────────┘│
│           ↓          │
│  ┌─────────────────┐│
│  │ Validate Data    │
│  │ Handle Errors    │
│  └─────────────────┘│
│           ↓          │
│  ┌─────────────────┐│
│  │ Transform Data   │
│  │ (JSON → CSV)     │
│  └─────────────────┘│
└─────────┬───────────┘
          │
          ▼
┌────────────────────  ┐
│  OUTPUT LAYER        │
│  - JSON file         │
│  - CSV file          │
│  - Logs              │
└───────────────────── ┘

┌────────────────────────────┐
│ 1. CLI (argparse)          │  User input / entry point
├────────────────────────────┤
│ 2. Validation & Config     │  Make sure inputs are safe
├────────────────────────────┤
│ 3. Rate Limiting           │  Prevent API abuse
├────────────────────────────┤
│ 4. Retry Logic             │  Recover from temporary failure
├────────────────────────────┤
│ 5. Circuit Breaker         │  Stop repeated failures
├────────────────────────────┤
│ 6. Business Logic          │  Fetch + process data
├────────────────────────────┤
│ 7. Logging & Metrics       │  Observability + debugging
└────────────────────────────┘


How Each Piece Fits Together
1. CLI Interface (Control Panel)

You tell the program:
- What to do (fetch, convert)
- With what (--cities, --file)
- How (--verbose, --format)

This replaces editing code manually.

2. Argument Parsing (Decision Layer)

argparse decides:
- Which function to call
- What parameters to pass
- What errors to show early

➡️ This protects your program from bad input.

3. Configuration Layer

Where environment & setup live:
- .env → secrets
- config.py → paths, constants
- logging setup

This makes the code portable and safe.

4. Core Logic (The Engine)

This is where real work happens:
- API requests
- Retry logic
- Error handling
- Data transformation

Think of this as the engine, not the interface.

5. Resilience Layer

What makes your code production-grade:
- Retry with backoff
- Timeout handling
- Graceful failures
- Partial success handling

This is the difference between scripts and systems.

6. Output Layer

Where results go:
- JSON for machines
- CSV for humans
- Logs for debugging

Everything is written intentionally and predictably.

