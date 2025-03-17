"""
Logging Utilities
---------------
Centralized logging configuration for the project.

Created: 2025-03-06
Author: David Dawson
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional, Union

# Type aliases
PathLike = Union[str, Path]

# Constants
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_LEVEL = logging.INFO


class CustomFormatter(logging.Formatter):
    """Custom formatter adding color to logging levels"""

    COLORS = {
        logging.DEBUG: "\033[0;36m",  # Cyan
        logging.INFO: "\033[0;32m",  # Green
        logging.WARNING: "\033[0;33m",  # Yellow
        logging.ERROR: "\033[0;31m",  # Red
        logging.CRITICAL: "\033[0;35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelno]}" f"{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(log_file: Optional[PathLike] = None, level: int = DEFAULT_LOG_LEVEL, module_name: Optional[str] = None) -> logging.Logger:
    """
    Configure logging with both file and console handlers.

    Args:
        log_file: Path to log file. If None, only console logging is setup.
        level: Logging level to use.
        module_name: Name for the logger. If None, uses the root logger.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(module_name or __name__)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Console handler with color formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter(LOG_FORMAT))
    logger.addHandler(console_handler)

    # File handler if log_file is specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=10485760, backupCount=5, encoding="utf-8")  # 10MB
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)

    return logger


# Create a top-level logger for the project
logger = setup_logging(level=DEFAULT_LOG_LEVEL, module_name="dwd_run")
