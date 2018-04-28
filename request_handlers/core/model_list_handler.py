#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

from components.base_handler import *


class ModelListHandler(BaseHandler):

	def get_model_list(self):
		model_list = []

		if self.get_service().get_model_list_check_sum() and (
				not self._data or 'check_sum' not in self._data or self._data.get(
				'check_sum', '') != self.get_service().get_model_list_check_sum()):
			model_list = self.get_service().get_model_list()

		self.write({
			'id': self.get_service().get_id(),
			'check_sum': self.get_service().get_model_list_check_sum(),
			'models': model_list
		})
		self.finish()

	async def post(self):
		self.get_model_list()

	async def get(self):
		self.get_model_list()
