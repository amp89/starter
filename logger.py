import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_SIZE_BYTES = 50*1000*1000
LOG_BACKUPS = 5

formatter = logging.Formatter('%(asctime)s|%(name)s|%(filename)s|%(lineno)s|%(levelname)s -  %(message)s')

log_path = Path(__file__).parent.absolute()/'logs'/'log.log'

logger = logging.getLogger('logger')
general_handler = RotatingFileHandler(log_path, maxBytes=LOG_SIZE_BYTES, backupCount=LOG_BACKUPS)
general_handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(general_handler)