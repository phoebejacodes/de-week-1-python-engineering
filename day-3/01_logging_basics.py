import logging

# Basic configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create logger
logger = logging.getLogger(__name__)

# Different severity levels

logger.debug("Debug message with timestamp")
logger.info("Info message with timestamp")
logger.warning("Warning message with timestamp")