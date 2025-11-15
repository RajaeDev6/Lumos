import logging
import os
from datetime import datetime

class AppLogger:
    def __init__(self, log_dir="logs", log_file="app.log"):
        self.log_dir = log_dir
        self.log_file = log_file
        os.makedirs(self.log_dir, exist_ok=True)
        
        log_path = os.path.join(self.log_dir, self.log_file)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - [%(levelname)s] - %(message)s",
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def exception(self, message: str):
        """Logs exception with traceback automatically."""
        self.logger.exception(message)

    def log_request(self, endpoint: str, method: str, status_code: int):
        """Logs API request details for debugging."""
        self.logger.info(f"Request -> {method} {endpoint} | Status: {status_code}")

    def log_event(self, event: str, details: str = ""):
        """General event logging (uploads, AI calls, etc.)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info(f"[{timestamp}] EVENT: {event} | DETAILS: {details}")


logger = AppLogger()
