import sys
import logging
import constants


class custom_logging:
    def __init__(self) -> None:

        logger_format = '%(levelname)s - %(asctime)s - %(message)s'

        logging.basicConfig(
            stream=sys.stdout,
            format=logger_format,
            level=logging.DEBUG)

        self.logger = logging.getLogger('main')

        file_handler = logging.FileHandler(constants.LOG_FILE_PATH)
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(logger_format)

        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.RootLogger:
        return self.logger

    def info(self, message):
        self.logger.info("{}".format(message))


my_logger = custom_logging().get_logger()
