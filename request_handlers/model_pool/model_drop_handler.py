#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.1"
__maintainer__ = "Maxim Morskov"
__site__ = "http://0mind.net"

from components.model_handler import *
from components.profiler import *
import psutil


class ModelDropHandler(ModelHandler):

	def unload_model(self):
		result = False
		unload_time = 0
		memory_delta = 0

		model_id = self.get_model_id()

		self.get_service().log().append('DROP', '{}: received request to drop the model id [{}]'.format(self.__class__.__name__, model_id))
		process = psutil.Process()
		memory_overview_before = process.memory_info()
		profiler = Profiler()
		self.get_service().remove_task(model_id)
		result = self.get_service().unload_model(model_id)
		if result:
			unload_time = profiler.get_timing()
			memory_overview_after = process.memory_info()
			memory_delta = memory_overview_before.rss - memory_overview_after.rss

		self.write({'result': bool(result), 'unload_time': unload_time, 'memory_released': memory_delta, 'model_id': model_id})
		self.finish()

	async def post(self):
		self.unload_model()

	async def get(self):
		self.unload_model()
