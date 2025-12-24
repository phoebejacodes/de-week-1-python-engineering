import requests
import json
import csv  

def fetch_users():
    """Fetch all users from the API."""
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    return response.json()

def fetch_posts_for_user(user_id):
    """Fetch all posts for a specific user."""
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        params={"userId": user_id}
    )
    return response.json()

def main():
    #Fetch all users
    users = fetch_users()
    print(f"Total users fetched: {len(users)}")

    #Collect all data
    all_data = []

    for user in users:
        posts = fetch_posts_for_user(user['id'])
        print(f"User {user['id']} - {user['name']} has {len(posts)} posts.")
        
        for post in posts:
            all_data.append({
                "user_id": user['id'],
                "user_name": user['name'],
                "post_id": post['id'],
                "post_title": post['title'],
                "post_body": post['body']
            })
    #Write to JSON file
    with open("user_posts.json", "w") as json_file:
        json.dump(all_data, json_file, indent=2)
    print(f"Wrote data for {len(all_data)} posts to user_posts.json")

    #Write to CSV file
    with open("user_posts.csv", "w", newline='') as csv_file:
        fieldnames = ["user_id", "user_name", "post_id", "post_title", "post_body"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for data in all_data:
            writer.writerow(data)
    print(f"Wrote data for {len(all_data)} posts to user_posts.csv")

if __name__ == "__main__":
    main()