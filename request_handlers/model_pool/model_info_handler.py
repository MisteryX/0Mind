#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"


from components.model_handler import *


class ModelInfoHandler(ModelHandler):

	def get_model_info(self):
		self.write(self.get_service().get_model(self.get_model_id()).get_specification())
		self.finish()

	def post(self):
		self.get_model_info()

	def get(self):
		self.get_model_info()
