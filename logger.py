import logging
from logging import StreamHandler
import sys

from datetime import datetime


class Log:
    def __init__(self):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        logging.basicConfig(filename=f'./logs/{timestamp}-log.txt', level=logging.DEBUG,
                            format='[%(asctime)s: %(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        stdout_handler = StreamHandler(sys.stdout)
        stdout_handler.setFormatter(logging.Formatter('[%(asctime)s: %(levelname)s] %(message)s',
                                                      datefmt='%Y-%m-%d %H:%M:%S'))
        self.logger = logging.getLogger()
        self.logger.addHandler(stdout_handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def exception(self, message):
        self.logger.exception(message)
