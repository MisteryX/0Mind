#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

from components.base_handler import *


class TasksInfoHandler(BaseHandler):

	def __get_tasks_info(self):
		result = {
			'id': self.get_service().get_id(),
			'tasks': self.get_service().get_tasks()
		}
		self.write(result)
		self.finish()

	def get(self):
		self.__get_tasks_info()

	def post(self):
		self.__get_tasks_info()
