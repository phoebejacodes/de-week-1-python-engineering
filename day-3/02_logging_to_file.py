import logging

# Configure logging to both console and file
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()  # Console
    ]
)

logger = logging.getLogger(__name__)

logger.info("Application started")
logger.debug("This is a debug message")
logger.warning("This is a warning")
logger.info("Application finished")