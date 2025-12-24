import requests

# Get posts by user 1
response1 = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"userId": 1}
)

posts = response1.json()
print(f"Posts by user 1: {len(posts)}")

for post in posts:
    print(f"  - {post['title']}")

# Get comments for post 1
response2 = requests.get(
    "https://jsonplaceholder.typicode.com/comments",
    params={"postId": 1}
)

comments = response2.json()
print(f"\nComments for post 1: {len(comments)}")
for comment in comments:
    print(f"  - {comment['name']} ({comment['email']})")


# Get all todos by user 3 that are completed

response3 = requests.get(
    "https://jsonplaceholder.typicode.com/todos",
    params={"userId": 3, "completed": True}
)

todos = response3.json()
print(f"\nCompleted todos by user 3: {len(todos)}")
for todo in todos:
    print(f"  - {todo['title']}")