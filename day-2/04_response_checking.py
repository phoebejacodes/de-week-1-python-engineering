import requests

def fetch_with_status_check(url):
    """Fetch URL and handle different status codes"""
    try:
        response = requests.get(url, timeout=10)
        
        # raise_for_status() throws an exception for 4xx/5xx codes (http errors)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Status Code: {e.response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None

# Test with valid URL
print("Valid URL:")
data = fetch_with_status_check("https://jsonplaceholder.typicode.com/posts/1")
print(f"  Got data: {data is not None}")

# Test with 404
print("\n404 URL:")
data = fetch_with_status_check("https://jsonplaceholder.typicode.com/posts/9999")
print(f"  Got data: {data is not None}")

# Test with invalid domain
print("\nInvalid domain:")
data = fetch_with_status_check("https://not-real-12345.com/api")
print(f"  Got data: {data is not None}")