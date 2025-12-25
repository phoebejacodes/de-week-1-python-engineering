# Week 1

## Day 2 — Error Handling and API Authentication  
**Theme:** *“My code doesn’t break when things go wrong.”*

Today’s focus was on understanding how APIs fail and how different classes of errors surface when making HTTP requests. Instead of assuming success, the goal was to observe and reason about failure modes explicitly.

---

## 1. Handling Invalid Endpoints (404 Not Found)

### Example

```python
import requests

response = requests.get("http://jsonplaceholder.typicode.com/not-real-endpoint")

print(f"Status Code: {response.status_code}")
print(f"Content: {response.text}")
###Observed Output
Status Code: 404
Content: {}

###Key Takeaways

A 404 status code means the server was reached, but the requested resource does not exist.
The request itself did not crash the program.
The API returned a valid HTTP response, just an unsuccessful one.
This type of error can be handled gracefully by checking response.status_code or using response.raise_for_status().
This is an example of a *recoverable API error.*

## 2. Authentication Errors (401 Unauthorized)

### Example 

response = requests.get(
    "http://api.openweathermap.org/data/2.5/weather?q=London&appid=INVALID_KEY"
)

print(f"Status Code: {response.status_code}")
print(f"Content: {response.text}")
###Observed Output
Status Code: 401
Content: {
  "cod": 401,
  "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."
}

###Key Takeaways

A 401 status code indicates an authentication failure.
The server was reachable and understood the request.
The request failed because credentials (API key) were invalid.
Error details are often returned in structured JSON, which can be parsed and logged.
Authentication errors should be explicitly handled and surfaced clearly in logs.

This is an example of a *client-side configuration error*, not a network failure.

## 3. Network / Connection Errors (Unreachable Domain)

### Example

response = requests.get("http://thisdomaindoesnotexist.tld")
###Observed Output
The program raises a ConnectionError.
No HTTP status code is returned.
Execution stops unless the error is caught.

###Key Takeaways

This is not an HTTP error — it is a network-level failure.
The request never reached a server.
These errors must be handled using try/except, not status code checks.
Common causes include:
DNS resolution failure
No internet connection
Incorrect domain name
This is an example of a *non-recoverable request failure* unless explicitly handled.

##Error Categories Observed
| Error Type             | Example              | Status Code | Crashes Program? |
| ---------------------- | -------------------- | ----------- | ---------------- |
| Invalid endpoint       | `/not-real-endpoint` | 404         | No               |
| Authentication failure | Invalid API key      | 401         | No               |
| Network failure        | Invalid domain       | None        | Yes              |

#The TCP/IP Model (4 Layers) 
## Application Layer – Combines OSI Layers 5, 6, and 7 into one. 
## Transport Layer – Same as OSI Layer 4. 
## Internet Layer – Same as OSI Layer 3. 
## Network Access Layer – Combines OSI Layers 1 and 2

###Application Layer (HTTP, APIs, business logic)

What this layer does
1.Handles HTTP requests and responses
2.Applies authentication
3.Executes application logic
4.Returns status codes and payloads

####Typical errors
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
500 Internal Server Error

###Transport Layer (TCP)

What this layer does
1.Establishes and maintains the connection
2.Ensures data is delivered
3.Handles timeouts and resets

####Typical errors
Connection timeout
Connection refused
Connection reset
TLS handshake failure

| Layer          | Failure Signal    | Get a Response?     |
| -------------- | ----------------- | ------------------- |
| Application    | HTTP status code  | ✅ Yes               |
| Transport      | Exception         | ❌ No                |
| Internet       | Wrapped exception | ❌ No                |
| Network Access | OS error          | ❌ No                |

##Python Exceptions: An Introduction
-Exceptions in Python occur when syntactically correct code results in an error.
-The try … except block, executes code and handle exceptions that arise.
-Use the else, and finally keywords for more refined exception handling.
-It’s bad practice to catch all exceptions at once using except Exception or the bare except clause.
-Combining try, except, and pass allows a program to continue silently without handling the exception.

## Exception Handling in Python

### `try` and `except`

The `try` block contains code that may fail at runtime.  
If an exception occurs, execution stops immediately and control moves to the matching `except` block.

```python
try:
    risky_operation()
except SomeException:
    handle_error()

-Only runtime errors raise exceptions

-Catch specific exceptions whenever possible

-If no exception is raised, except is skipped

### else

The else block runs only if no exception occurred in the try block.

try:
    operation()
except Exception:
    handle_error()
else:
    process_result()

###finally

The finally block always runs, regardless of success or failure.

try:
    operation()
finally:
    cleanup()

Used for:
-closing files
-releasing resources
-cleanup logic

##Key Takeaway

try → attempt risky work

except → handle failure

else → run only on success

finally → always clean up

Exception handling is about controlling failure, not avoiding it.


