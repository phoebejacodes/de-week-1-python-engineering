import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")
users= response.json()


for user in users:
    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"City: {user['address']['city']}")
    print(f"Latitude: {user['address']['geo']['lat']}")
    print(f"Company: {user['company']['name']}")