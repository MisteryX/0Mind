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
from components.profiler import *
import psutil


class ModelLoadHandler(BaseHandler):
	_attributes = None

	def initialize(self, service):
		super(ModelLoadHandler, self).initialize(service)
		self._attributes = self.get_service().get_pool_task_attributes()

	async def post(self):
		result = False
		load_time = 0
		memory_delta = 0

		if not self._data:
			self._raise_error(
				500,
				[MindError(
					MindError.CODE_REQUEST_MODEL_LOAD_HAS_NO_DATA,
					'{}: No data is specified to load a model',
					[self.__class__.__name__]
				)]
			)
		model_id = self._data.get('id')
		if self.get_service().is_model_exists(model_id):
			self._raise_error(
				500,
				[MindError(
					MindError.CODE_REQUEST_MODEL_HAS_BEEN_ALREADY_LOADED,
					'{}: Model id [{}] has been already loaded in this pool',
					[self.__class__.__name__, model_id]
				)]
			)

		try:
			self.get_service().log().append('{}: received request to load the model id [{}]'.format(self.__class__.__name__, model_id))
			process = psutil.Process()
			memory_overview = process.memory_info()
			profiler = Profiler()
			result = self.get_service().load_model(self._data, validate=False, raise_exception=True)
			if result:
				self.get_service().append_task(self._data)
				load_time = profiler.get_timing()
				memory_view = process.memory_info()
				memory_delta = memory_view.rss - memory_overview.rss
		except MindException as ex:
			self._raise_error(500, ex.get_errors())
		except Exception as ex:
			self._raise_error(
				500,
				[MindError(
					MindError.CODE_REQUEST_UNKNOWN_LOAD_MODEL_ERROR,
					'{}: ' + ', '.join(ex.args),
					[self.__class__.__name__]
				)]
			)

		self.write({'result': bool(result), 'load_time': load_time, 'memory_consumed': memory_delta, 'model_id': model_id})
		self.finish()
