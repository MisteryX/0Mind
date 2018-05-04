#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.1"
__maintainer__ = "Maxim Morskov"
__site__ = "http://0mind.net"

from components.base_handler import *


class TasksInfoHandler(BaseHandler):

	def __get_tasks_info(self)->dict:
		return {
			'id': self.get_service().get_id(),
			'tasks': self.get_service().get_tasks()
		}

	def get(self):
		self.write(self.__get_tasks_info())
		self.finish()

	def post(self):
		self.write(self.__get_tasks_info())
		self.finish()
