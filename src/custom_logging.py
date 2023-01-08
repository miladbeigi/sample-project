import sys
import logging
import constants


class custom_logging:
    def __init__(self) -> None:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(constants.LOG_FILE_PATH, mode="w")
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.RootLogger:
        return self.logger