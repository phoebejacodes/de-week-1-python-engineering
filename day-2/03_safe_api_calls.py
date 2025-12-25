import requests

def fetch_post(post_id):
    """Fetch a post with error handling"""
    try:
        response = requests.get(
            f"https://jsonplaceholder.typicode.com/posts/{post_id}",
            timeout=10  # Always set a timeout!
        )
        
        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Post {post_id} not found")
            return None
        else:
            print(f"Unexpected status: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"Request timed out for post {post_id}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Connection failed for post {post_id}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Test it
print("Fetching valid post:")
post = fetch_post(1)
if post:
    print(f"  Title: {post['title']}")

print("\nFetching invalid post:")
post = fetch_post(9999)
if post:
    print(f"  Title: {post['title']}")
else:
    print("  No post returned")