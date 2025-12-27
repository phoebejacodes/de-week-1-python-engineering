import time
import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

class CircuitBreaker:
    """
    Circuit breaker pattern implementation
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Service is down, fail fast without trying
    - HALF_OPEN: Testing if service recovered
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.successes = 0
        self.last_failure_time = None
    
    def can_execute(self) -> bool:
        """Check if we should attempt the operation"""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if self.last_failure_time:
                time_since_failure = datetime.now() - self.last_failure_time
                if time_since_failure > timedelta(seconds=self.recovery_timeout):
                    logger.info("Circuit breaker: OPEN -> HALF_OPEN (testing recovery)")
                    self.state = CircuitState.HALF_OPEN
                    return True
            return False
        
        if self.state == CircuitState.HALF_OPEN:
            return True
        
        return False
    
    def record_success(self):
        """Record a successful call"""
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self.success_threshold:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED (recovered)")
                self.state = CircuitState.CLOSED
                self.failures = 0
                self.successes = 0
        else:
            self.failures = 0
    
    def record_failure(self):
        """Record a failed call"""
        self.failures += 1
        self.last_failure_time = datetime.now()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (still failing)")
            self.state = CircuitState.OPEN
            self.successes = 0
        elif self.failures >= self.failure_threshold:
            logger.warning(f"Circuit breaker: CLOSED -> OPEN (threshold reached: {self.failures} failures)")
            self.state = CircuitState.OPEN
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        if not self.can_execute():
            raise Exception(f"Circuit breaker is OPEN - request rejected")
        
        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise

# Demo
def unreliable_service(fail_rate=0.7):
    """Simulates an unreliable service"""
    import random
    if random.random() < fail_rate:
        raise Exception("Service unavailable")
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    breaker = CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=10,
        success_threshold=2
    )
    
    print("=== Testing Circuit Breaker ===")
    print("(Service has 70% failure rate)")
    print()
    
    for i in range(20):
        print(f"Request {i+1}: State={breaker.state.value}", end=" -> ")
        
        try:
            result = breaker.execute(unreliable_service)
            print("SUCCESS")
        except Exception as e:
            print(f"FAILED: {e}")
        
        time.sleep(1)