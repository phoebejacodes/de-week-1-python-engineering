import requests
import json
import csv


def fetch_todos():
    """Fetch all todos from the API."""
    todosurl = "https://jsonplaceholder.typicode.com/todos"
    response = requests.get(todosurl)
    return response.json()

def fetch_user(user_id):
    """Fetch a specific user from the API."""
    usersurl = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(usersurl + f"/{user_id}")
    return response.json()

def main():
    # Fetch all todos
    todos = fetch_todos()
    print(f"Total todos fetched: {len(todos)}")

    # Find unique user IDs
    unique_user_ids = set(todo['userId'] for todo in todos)
    print(f"Unique user IDs found: {len(unique_user_ids)}")
    
    #Fetch each user once (build lookup table)
    users = {}
    for user_id in unique_user_ids:
        users[user_id] = fetch_user(user_id)

    # Combine todos with user data
    all_data = []

    for todo in todos:
        user = users[todo['userId']]
    
        all_data.append({
            "user_id": user['id'],
            "user_name": user['name'],
            "todo_id": todo['id'],
            "todo_title": todo['title'],
            "todo_completed": todo['completed'],
            "user_email": user['email']

        })
    

    # Write to JSON file
    with open("user_todos.json", "w") as json_file:
        json.dump(all_data, json_file, indent=2)
    print(f"Wrote data for {len(all_data)} todos to user_todos.json")

    # Write to CSV file
    with open("user_todos.csv", "w", newline='') as csv_file:
        fieldnames = ["user_id", "user_name", "todo_id", "todo_title", "todo_completed", "user_email"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for data in all_data:
            writer.writerow(data)
    print(f"Wrote data for {len(all_data)} todos to user_todos.csv")

if __name__ == "__main__":
    main() 

