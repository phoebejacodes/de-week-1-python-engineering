import requests
response1 = requests.get("https://jsonplaceholder.typicode.com/posts/1")

#Convert JSON response to dictionary
data=response1.json()

print (f"Types of data: {type(data)}")
print (f"Keys in data: {data.keys()}")
print (f"Title: {data['title']}")
print (f"Body: {data['body']}")
print (f"User ID: {data['userId']}")

responseposts = requests.get("https://jsonplaceholder.typicode.com/posts")
posts = responseposts.json()

print (f"Total posts: {len(posts)}")
print (f"Type of posts data: {type(posts)}")
print (f"First post: {posts[0]}")
print (f"Title of first post: {posts[0]['title']}")

for post in posts:
    print(f"Post {post['id']}: {post['title']}")