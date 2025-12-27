import requests
import time

def demonstrate_failures():
    """Show different types of failures"""
    
    # 1. Timeout
    print("=== Testing Timeout ===")
    try:
        # httpbin.org/delay/10 waits 10 seconds before responding
        response = requests.get("https://httpbin.org/delay/10", timeout=2)
        print(f"Success: {response.status_code}")
    except requests.exceptions.Timeout:
        print("FAILED: Request timed out (expected)")
    
    # 2. Connection error
    print("\n=== Testing Connection Error ===")
    try:
        response = requests.get("https://not-a-real-domain-12345.com", timeout=5)
        print(f"Success: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("FAILED: Connection error (expected)")
    
    # 3. HTTP errors
    print("\n=== Testing HTTP Errors ===")
    
    # 404 Not Found
    response = requests.get("https://httpbin.org/status/404")
    print(f"404 Status: {response.status_code}")
    
    # 500 Server Error
    response = requests.get("https://httpbin.org/status/500")
    print(f"500 Status: {response.status_code}")
    
    # 429 Rate Limited
    response = requests.get("https://httpbin.org/status/429")
    print(f"429 Status: {response.status_code}")
    
    # 4. Successful request
    print("\n=== Testing Success ===")
    response = requests.get("https://httpbin.org/json", timeout=10)
    print(f"Success: {response.status_code}")

if __name__ == "__main__":
    demonstrate_failures()