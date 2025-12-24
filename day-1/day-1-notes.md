# Week 1 

## Day 1
### Python 3rd part Request Library
This library makes http requests in Python.


---
>>>request.get("https://api.github.com")
--- <Response[200]>
---
>>>response = requests.get("https://api.github.com")
---
---
>>>response.text
---
*returns a string*
---
>>>response.context
---
*returns raw bytes*

#### Status Code

---
<Response[200]>
*means OK*
<Response [404]>
*means not found*

to access status code:
---
>>>response.status_code
---
---
>>>if response.status_code == 200:
>>>     print ("Success")
>>>elif response.status_code == 404:
>>>     print ("Not found")
---
Requests goes one step further in simplifying this process for you. If you use a Response instance in a Boolean context, such as a conditional statement, then it’ll evaluate to True when the status code is less than 400, and False otherwise.

That means you can modify the last example by rewriting the if statement:
---
>>>if response:
>>>     print("Success")
>>>else:
>>>     raise Exception(f"Non-success status code: {response.status_code}")
---
To use Request’s built-in capacities to raise an exception if the request was unsuccessful. :
---
>>>response.raise_for_status()
---

### Access the Response Content

To see the response’s content in bytes, you use .content:
---
>>> response.content
*b'{"current_user_url":"https://api.github.com/user", ...}'*

>>> type(response.content)
*<class 'bytes'>*
---
To provide an explicit encoding by setting .encoding before accessing .text:
---
>>> response.encoding = "utf-8"  # Optional: Requests infers this.
>>> response.text
*'{"current_user_url":"https://api.github.com/user", ...}'*
---
To get a dictionary, take the str retrieved from .text and deserialize it using json.loads(). However, the direct way to accomplish this task is to use .json():
---
>>> response.json()
*{'current_user_url': 'https://api.github.com/user', ...}*

>>> type(response.json())
*<class 'dict'>*
---
The type of the return value of .json() is a dictionary, access values in the object by key:
---
>>> response_dict = response.json()
>>> response_dict["emojis_url"]
*'https://api.github.com/emojis'*
---

### View Response Headers

To view headers, access .headers:
---
>>> import requests

>>> response = requests.get("https://api.github.com")
>>> response.headers
*{'Server': 'github.com',
...
'X-GitHub-Request-Id': 'AE83:3F40:2151C46:438A840:65C38178'}*
---
The .headers attribute returns a dictionary-like object, allows to access header values by key.

### Add Query String Parameters

To modify results from the .get, pass a dictionary or tuple to PARAMS.
#### Dictionary:
---
>>>import requests

>>>response = requests.get(
    *"https://api.github.com/search/repositories",
    params={"q": "language:python", "sort": "stars", "order": "desc"},
)*

>>>json_response = response.json()
>>>popular_repositories = json_response["items"]
>>>for repo in popular_repositories[:3]:
>>>    print(f"Name: {repo['name']}")
>>>    print(f"Description: {repo['description']}")
>>>    print(f"Stars: {repo['stargazers_count']}\n")
---

#### List of tuples:
---
>>> import requests

>>> requests.get(
...     "https://api.github.com/search/repositories",
...     [("q", "language:python"), ("sort", "stars"), ("order", "desc")],
... )
*<Response [200]>*
---