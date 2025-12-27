import requests
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def fetch_with_retry(url, max_retries=3, timeout=10):
    """
    Fetch URL with simple retry logic
    """
    for attempt in range(1, max_retries + 1):
        logger.info(f"Attempt {attempt}/{max_retries}: {url}")
        
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            logger.info(f"Success on attempt {attempt}")
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.warning(f"Attempt {attempt} timed out")
        except requests.exceptions.ConnectionError:
            logger.warning(f"Attempt {attempt} connection failed")
        except requests.exceptions.HTTPError as e:
            logger.warning(f"Attempt {attempt} HTTP error: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
        
        # Wait before retry (except on last attempt)
        if attempt < max_retries:
            wait_time = 2  # Fixed 2 second wait
            logger.info(f"Waiting {wait_time}s before retry...")
            time.sleep(wait_time)
    
    logger.error(f"All {max_retries} attempts failed")
    return None

# Test with a working URL
print("=== Test 1: Working URL ===")
data = fetch_with_retry("https://httpbin.org/json")
if data:
    print(f"Got data: {list(data.keys())}")

# Test with failing URL
print("\n=== Test 2: Failing URL ===")
data = fetch_with_retry("https://httpbin.org/status/500")
print(f"Result: {data}")