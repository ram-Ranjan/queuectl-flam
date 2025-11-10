import os
import logging

LOG_DIR = "job_logs"

def get_logger(job_id: str):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_file = os.path.join(LOG_DIR, f"{job_id}.log")
    logger = logging.getLogger(job_id)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
