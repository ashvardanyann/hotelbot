import logging

logger = logging.getLogger('rootlogger')
logger.setLevel(logging.DEBUG)

handler_formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]')

error_handler = logging.FileHandler('errors.log', encoding='utf-8')
error_handler.setFormatter(handler_formatter)

logger.addHandler(error_handler)
