import logging
from datetime import datetime
import os

## month-date-time
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

## path setting
log_path = os.path.join(os.getcwd(), "logs")

## making directory
os.makedirs(log_path, exist_ok=True)

## log file path
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

## logging method
logging.basicConfig(
    level =logging.INFO,
    filename= LOG_FILEPATH,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)