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
from ML.adapters.base_model import BaseModel


class ModelPredictHandler(ModelHandler):

	async def post(self):

		if not self.get_data() or len(self.get_data()) == 0:
			self._raise_error(400, '{}: Wrong request! Data is empty'.format(self.__class__.__name__))

		model = self.get_service().get_model(self.get_model_id())

		if model is None or not isinstance(model, BaseModel):
			self._raise_error(413, 'No idle instances of model_id={}. Try again later.'.format(self.get_model_id()))

		result = {}
		model_time = 0

		model.clear_errors()
		try:
			profiler = Profiler()
			result = await self.__get_predict(model, self.get_data())
			model_time = profiler.get_timing()
		except Exception as ex:
			self._raise_error(500, str(ex.args))

		if model.has_errors():
			errors = model.get_errors()
			self._raise_error(500, 'model_id={}: {}'.format(self.get_model_id(), errors))

		self.write({
			'result': result,
			'model_time': model_time
		})
		self.finish()

	@staticmethod
	async def __get_predict(model: BaseModel, data):
		return model.predict(data)

