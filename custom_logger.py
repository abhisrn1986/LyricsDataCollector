import logging
import logging.config

logging.config.fileConfig('logging.conf')


def get_custom_named_logger(name: str):
	return logging.getLogger(name)
