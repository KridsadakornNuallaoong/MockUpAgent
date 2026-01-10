import os

import logger

path_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(path_dir, "logger.log")

logger = logger.Logger(
    log_file_path=log_file_path,
    console_log_level="DEBUG",
    file_log_level="DEBUG",
)