import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name (e.g. 20260704.log)
LOG_FILE = f"{datetime.now().strftime('%Y%m%d')}.log"

# Complete log file path
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s"
)

# Create logger object
logger = logging.getLogger()