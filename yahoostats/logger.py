import logging
from logging.config import fileConfig
from os import path
fileConfig(path.join('yahoostats', 'logging_config.ini'))
logger = logging.getLogger()
