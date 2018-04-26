#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

try:
	import redis
except ImportError as e:
	pass
import argparse
import json
from helpers.file_helper import *
import logging as log
from logging import config
from datetime import *
import os

DEFAULT_CONFIG_FILE = 'configs/logger.json'


class EventLog:
	__config = None
	__redis = None
	__name = ""

	def __init__(self, name, redis_config=None, logger_config=None):
		self.__name = name

		if logger_config is None:
			self.__config = json.loads(FileHelper.get_text_file_content(DEFAULT_CONFIG_FILE))
			if redis_config is not None:
				self.__config['redis_config'] = redis_config
		else:
			self.__config = {'logger_config': logger_config, 'redis_config': redis_config, 'name': name}

		if 'handlers' in self.__config['logger_config'] and 'default' in self.__config['logger_config']['handlers']:
			self.__config['logger_config']['handlers']['default']['filename'] = 'logs/' + self.get_name() + '.log'

		if 'redis_config' in self.__config and self.__config['redis_config'] is not None:
			self.__redis = redis.StrictRedis(**self.__config['redis_config'])

		log.config.dictConfig(self.__config['logger_config'])

		self.append('Logger INIT')

	def get_name(self):
		return self.__name

	def append(self, message='', log_level=log.INFO):
		result = False
		_logger = self.get_logger()
		if _logger is not None:
			_logger.log(log_level, message)
		return result

	def get_logger(self):
		return log.getLogger(self.get_name())

	def get_config(self):
		return self.__config

	def __get_redis_key(self):
		return 'status_' + self.get_name()


def get_params_using_parser(args: list):
	params_parser = argparse.ArgumentParser()
	params_parser.add_argument(
		'-c', '--config_file',
		type=str, help='path to config file',
		default=DEFAULT_CONFIG_FILE
	)
	return params_parser.parse_args()


# --== Entry point ==--
if __name__ == "__main__":
	params = get_params_using_parser(sys.argv[1:])
	logger = EventLog(
		**json.loads(FileHelper.get_text_file_content(params.config_file))
	)
