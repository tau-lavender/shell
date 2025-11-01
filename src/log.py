from src.configs.logger_config import LOGGING_CONFIG
import logging.config


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def report_error(text):
    logger.error(text)
    print(text)
