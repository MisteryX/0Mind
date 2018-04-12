#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Maxim Morskov"
__site__ = "http://0mind.net"

from components.base_handler import *
import sys


class SystemInfoHandler(BaseHandler):

	def __get_sys_info(self)->dict:
		return {
			'id': self.get_service().get_id(),
			'cpu_usage': self.get_service().get_current_cpu_usage(),
			'memory': self.get_service().get_memory_info(),
			'python': list(sys.version_info)
		}

	def get(self):
		self.write(self.__get_sys_info())
		self.finish()

	def post(self):
		self.write(self.__get_sys_info())
		self.finish()

