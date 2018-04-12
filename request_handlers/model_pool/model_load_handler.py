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
from components.profiler import *
import psutil


class ModelLoadHandler(BaseHandler):
	def initialize(self, service):
		super(ModelLoadHandler, self).initialize(service)
		self._attributes = self.get_service().get_pool_task_attributes()

	async def post(self):
		result = False
		load_time = 0
		memory_delta = 0

		if not self._data:
			self._raise_error(500, '{}: No data is specified to load a model'.format(self.__class__.__name__))
		model_id = self._data.get('id')
		if self.get_service().is_model_exists(model_id):
			self._raise_error(500, '{}: Model id [{}] has been already loaded in this pool'.format(self.__class__.__name__, model_id))

		try:
			self.get_service().log().append('LOADING', '{}: received request to load the model id [{}]'.format(self.__class__.__name__, model_id))
			process = psutil.Process()
			memory_overview = process.memory_info()
			profiler = Profiler()
			result = self.get_service().load_model(self._data, validate=False, raise_exception=True)
			if result:
				self.get_service().append_task(self._data)
				load_time = profiler.get_timing()
				memory_view = process.memory_info()
				memory_delta = memory_view.rss - memory_overview.rss
		except Exception as ex:
			self._raise_error(500, '{}: {}'.format(self.__class__.__name__, ', '.join(ex.args)))

		self.write({'result': bool(result), 'load_time': load_time, 'memory_consumed': memory_delta, 'model_id': model_id})
		self.finish()
