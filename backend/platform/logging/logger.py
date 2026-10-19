import logging
import sys
from datetime import datetime

# Custom logger configuration for OpsPilot AI
logger = logging.getLogger('opspilot')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_logger(name):
    """Returns a named logger configured with the platform's standard format."""
    return logging.getLogger(f'opspilot.{name}')
