import logging
import colorlog

# Configure the logging settings
LOG_FORMAT = "%(asctime)s |%(log_color)s%(levelname)s%(reset)s| %(message)s"
colorlog.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

# Create a logger
logger = colorlog.getLogger()

