import requests

#This URL is intentionally incorrect to demonstrate error handling
response = requests.get("http://jsonplaceholder.typicode.com/not-real-endpoint")
print (f"Status Code: {response.status_code}")
print (f"Content: {response.text}")
#Status Code: 404
#Content: {}
#print("-"*40)

#This key is invalid, which will likely raise an authentication error
response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=London&appid=INVALID_KEY")
print (f"Status Code: {response.status_code}")
print (f"Content: {response.text}")
#Status Code: 401
#Content: {"cod":401, "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."}
#print("-"*40)

#This domain does not exist, which will raise a ConnectionError
response = requests.get("http://thisdomaindoesnotexist.tld")
print (f"Status Code: {response.status_code}")
print (f"Content: {response.text}")
#Status Code: <unreachable> System crashes with ConnectionError
#print("-"*40)

