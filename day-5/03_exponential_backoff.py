import requests
import time
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def fetch_with_backoff(url, max_retries=5, base_delay=1, max_delay=60, timeout=10):
    """
    Fetch URL with exponential backoff and jitter
    
    Args:
        url: URL to fetch
        max_retries: Maximum number of attempts
        base_delay: Starting delay in seconds
        max_delay: Maximum delay (cap)
        timeout: Request timeout
    """
    for attempt in range(1, max_retries + 1):
        logger.info(f"Attempt {attempt}/{max_retries}")
        
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            logger.info(f"Success on attempt {attempt}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            
            if attempt < max_retries:
                # Calculate delay with exponential backoff
                delay = base_delay * (2 ** (attempt - 1))
                
                # Add jitter (randomness) to prevent thundering herd
                jitter = random.uniform(0, delay * 0.1)
                delay = min(delay + jitter, max_delay)
                
                logger.info(f"Waiting {delay:.2f}s before retry...")
                time.sleep(delay)
    
    logger.error(f"All {max_retries} attempts failed")
    return None

def calculate_backoff_schedule(max_retries=5, base_delay=1):
    """Show what the backoff schedule looks like"""
    print("Backoff Schedule:")
    for attempt in range(1, max_retries + 1):
        delay = base_delay * (2 ** (attempt - 1))
        print(f"  After attempt {attempt}: wait ~{delay}s")

# Show the schedule
calculate_backoff_schedule()

print("\n=== Testing with failing endpoint ===")
# This will fail and show exponential backoff
data = fetch_with_backoff("https://httpbin.org/status/503", max_retries=4)