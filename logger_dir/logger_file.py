import logging


# Создание люггера
logger = logging.getLogger('rootlogger')
logger.setLevel(logging.DEBUG)

handler_formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]')

# Создание обработчика
error_handler = logging.FileHandler('errors.log', encoding='utf-8')
error_handler.setFormatter(handler_formatter)

# Добавляем обработчик
logger.addHandler(error_handler)
