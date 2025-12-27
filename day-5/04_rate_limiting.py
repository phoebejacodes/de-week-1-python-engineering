import requests
import time
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple rate limiter using token bucket algorithm"""
    
    def __init__(self, calls_per_second=1):
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0
    
    def wait(self):
        """Wait if necessary to respect rate limit"""
        now = time.time()
        elapsed = now - self.last_call
        
        if elapsed < self.min_interval:
            wait_time = self.min_interval - elapsed
            logger.debug(f"Rate limiting: waiting {wait_time:.2f}s")
            time.sleep(wait_time)
        
        self.last_call = time.time()

def fetch_with_rate_limit(url, rate_limiter, max_retries=3, timeout=10):
    """Fetch URL with rate limiting and retry logic"""
    
    for attempt in range(1, max_retries + 1):
        # Wait for rate limit
        rate_limiter.wait()
        
        try:
            response = requests.get(url, timeout=timeout)
            
            # Handle rate limit response
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                logger.warning(f"Rate limited. Waiting {retry_after}s")
                time.sleep(retry_after)
                continue
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
    
    return None

def fetch_many(urls, calls_per_second=2):
    """Fetch multiple URLs with rate limiting"""
    rate_limiter = RateLimiter(calls_per_second=calls_per_second)
    results = []
    
    logger.info(f"Fetching {len(urls)} URLs at {calls_per_second}/second")
    start_time = time.time()
    
    for i, url in enumerate(urls):
        logger.info(f"Fetching {i+1}/{len(urls)}: {url}")
        data = fetch_with_rate_limit(url, rate_limiter)
        if data:
            results.append(data)
    
    elapsed = time.time() - start_time
    logger.info(f"Completed {len(results)}/{len(urls)} in {elapsed:.2f}s")
    
    return results

# Test
urls = [
    "https://httpbin.org/json",
    "https://httpbin.org/json",
    "https://httpbin.org/json",
    "https://httpbin.org/json",
    "https://httpbin.org/json",
]

print("=== Fetching with rate limit (2/second) ===")
results = fetch_many(urls, calls_per_second=2)
print(f"\nGot {len(results)} results")