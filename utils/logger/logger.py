import logging
import os
from os import getenv

log_path = getenv("LOG_PATH", "./logs")
log_file = getenv("LOG_FILE", "app.log")
log_name = getenv("LOG_NAME", "app_logger")
os.makedirs(log_path, exist_ok=True)

logger = logging.getLogger(log_name)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(log_path, log_file), encoding='utf-8')
formatter = logging.Formatter(
    '%(asctime)s - [%(name)s] - [%(levelname)s] - %(message)s'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info("Logger initialized")