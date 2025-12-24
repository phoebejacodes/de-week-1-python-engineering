# Week 1

## Day 1

### Python Third-Party Requests Library

The `requests` library makes HTTP requests in Python.

---

## Making a GET Request

```python
import requests

requests.get("https://api.github.com")
Returns:
<Response [200]>

response = requests.get("https://api.github.com")
Accessing Response Text

response.text
Returns a string.


response.content
Returns raw bytes.

Status Codes
<Response [200]> → OK

<Response [404]> → Not Found

Access the status code:


response.status_code
Example:


if response.status_code == 200:
    print("Success")
elif response.status_code == 404:
    print("Not found")
Boolean Evaluation of Responses
A Response object evaluates to:

True if the status code is less than 400

False otherwise

Example:


if response:
    print("Success")
else:
    raise Exception(f"Non-success status code: {response.status_code}")
Raising Exceptions Automatically
Use Requests’ built-in method to raise an exception for unsuccessful requests:


response.raise_for_status()
Accessing the Response Content
To see the response content in bytes:


response.content

b'{"current_user_url":"https://api.github.com/user", ...}'

type(response.content)
<class 'bytes'>
Setting Encoding Explicitly

You can set encoding before accessing .text:


response.encoding = "utf-8"  # Optional: Requests usually infers this
response.text

'{"current_user_url":"https://api.github.com/user", ...}'
Parsing JSON Responses
The recommended way to parse JSON is using .json():


response.json()

{'current_user_url': 'https://api.github.com/user', ...}

type(response.json())

<class 'dict'>
Access values by key:


response_dict = response.json()
response_dict["emojis_url"]
'https://api.github.com/emojis'
Viewing Response Headers

response.headers
Example:


response.headers["Server"]
Headers are returned as a dictionary-like object.

Adding Query String Parameters
You can pass query parameters using a dictionary:

python:
response = requests.get(
    "https://api.github.com/search/repositories",
    params={
        "q": "language:python",
        "sort": "stars",
        "order": "desc"
    }
)

json_response = response.json()
popular_repositories = json_response["items"]

for repo in popular_repositories[:3]:
    print(f"Name: {repo['name']}")
    print(f"Description: {repo['description']}")
    print(f"Stars: {repo['stargazers_count']}\n")
### Query Parameters as a List of Tuples

```python
requests.get(
    "https://api.github.com/search/repositories",
    params=[
        ("q", "language:python"),
        ("sort", "stars"),
        ("order", "desc")
    ]
)
```

```
<Response [200]>
```
