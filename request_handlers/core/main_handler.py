#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

from components.base_handler import *
from helpers.version_helper import VersionHelper


class MainHandler(BaseHandler):

	def __get_service_info(self)->dict:
		return {
			'service': self.get_service().__class__.__name__,
			'id': self.get_service().get_id(),
			'options': self.get_service().get_options(),
			'version': VersionHelper.get_current_version()
		}

	def get(self):
		self.write(self.__get_service_info())
		self.finish()

	def post(self):
		self.write(self.__get_service_info())
		self.finish()

