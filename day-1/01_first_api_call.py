from urllib import response
import requests
response1 = requests.get("https://jsonplaceholder.typicode.com/posts/1")

print (f"Status Code: {response1.status_code}")
print (f"Headers: {response1.headers}")
print (f"Content: {response1.text}")

response2 = requests.get("https://jsonplaceholder.typicode.com/posts/2")

print (f"Status Code: {response2.status_code}")
print (f"Headers: {response2.headers}")
print (f"Content: {response2.text}")

response999 = requests.get("https://jsonplaceholder.typicode.com/posts/999")

print (f"Status Code: {response999.status_code}")
print (f"Headers: {response999.headers}")
print (f"Content: {response999.text}")

responseuser1 = requests.get("https://jsonplaceholder.typicode.com/users/1")

print (f"Status Code: {responseuser1.status_code}")
print (f"Headers: {responseuser1.headers}")
print (f"Content: {responseuser1.text}")

responsecomments1 = requests.get("https://jsonplaceholder.typicode.com/comments/1")

print (f"Status Code: {responsecomments1.status_code}")
print (f"Headers: {responsecomments1.headers}")
print (f"Content: {responsecomments1.text}")        


