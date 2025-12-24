import requests
import json

#Get all posts
response = requests.get("https://jsonplaceholder.typicode.com/posts")
posts = response.json()

#Write RAW JSON response to file
with open("posts.json", "w") as f:
    json.dump(posts, f, indent=2)

print(f"Wrote {len(posts)} posts to posts.json")

import csv

#Write posts to CSV file
with open("posts.csv", "w", newline='') as f:
    writer = csv.DictWriter(f,fieldnames=["id", "userID", "title", "body"])
    #Write header
    writer.writeheader()
    #Write data rows
    for post in posts:
        writer.writerow({"id": post["id"], "userID": post["userId"], "title": post["title"], "body": post["body"]})

print(f"Wrote {len(posts)} posts to posts.csv")
