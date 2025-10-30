from src.configs.logger_config import LOGGING_CONFIG
import logging.config


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
