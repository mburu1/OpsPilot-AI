import logging
import sys

logger = logging.getLogger("opspilot")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.addHandler(handler)

def get_logger(name):
    """Return a logger using the standard OpsPilot namespace."""
    return logging.getLogger(f"opspilot.{name}")
