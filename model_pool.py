#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Maxim Morskov"
__site__ = "http://0mind.net"

import argparse
import json

from helpers.file_helper import *
from tornado import web
from ML.model_factory import ModelFactory
from components.service import Service
from components.mind_exception import *
from request_handlers.core.main_handler import *
from request_handlers.core.system_info_handler import *
from request_handlers.core.task_info_handler import *
from request_handlers.model_pool.model_predict_handler import *
from request_handlers.model_pool.model_load_handler import *
from request_handlers.model_pool.model_drop_handler import *
from request_handlers.model_pool.model_info_handler import *
from request_handlers.core.model_list_handler import *
from request_handlers.model_pool.command_stop_handler import *


class ModelPool(Service):
	__models = {}

	def __init__(self, id, host, port, tasks, **options):
		super().__init__(id=id, host=host, port=port, tasks=tasks, **options)

		models_count = self.__load_models()
		self.log().append('{} model(s) was(were) loaded to {}'.format(models_count, self.__class__.__name__))

		self._init_service()

	def _init_service(self):
		self.log().append('Starting server on port {}'.format(self.get_port()))
		__server = tornado.web.Application(
			[
				(r"/info", MainHandler, {'service': self}),
				(r"/info/system", SystemInfoHandler, {'service': self}),
				(r"/info/tasks", TasksInfoHandler, {'service': self}),
				(r"/model/predict", ModelPredictHandler, {'service': self}),
				(r"/model/list", ModelListHandler, {'service': self}),
				(r"/model/load", ModelLoadHandler, {'service': self}),
				(r"/model/drop", ModelDropHandler, {'service': self}),
				(r"/model/info", ModelInfoHandler, {'service': self}),
				(r"/command/stop", CommandStopHandler, {'service': self})
			],
			default_handler_class=MainHandler, debug=bool(self.get_option('debug'))
		)
		__server.listen(self.get_port(), address=self.get_host())
		self.set_server(__server)
		self.log().append('{}:{} service is ready to run'.format(self.__class__.__name__, self.get_id()))

	def __append_model(self, _id: str, model: BaseModel):
		self.__models[_id] = model
		self.log().append('Model id [{}] has been loaded successfully'.format(_id))

	def load_model(self, task: dict, validate=True, raise_exception=False)->bool:
		try:
			if validate:
				is_task_valid, wrong_attribute = self._is_dictionary_valid(task, self.get_pool_task_attributes())
				if not is_task_valid:
					raise MindException(
						MindError(
							MindError.CODE_TASK_VALIDATION,
							'Compulsory task attribute [{}] not found in the task {}',
							[wrong_attribute, str(task)]
						)
					)

			if self.get_option('model_types') and task['model_type'] not in self.get_option('model_types'):
				raise MindException(
					MindError(
						MindError.CODE_UNSUPPORTED_MODEL_TYPE,
						'Task id [{}] has unsupported type [{}] so can`t be loaded',
						[task['id'], task['model_type']]
					)
				)

			self.log().append('Loading the task: {}'.format(str(task)))

			model = ModelFactory().get_model(**task)

			if model.has_errors():
				raise Exception(model.get_errors())
			self.__append_model(task['id'], model)
			self.model_list_check_sum_update()
		except Exception as ex:
			self.log().append(', '.join(ex.args), log.ERROR)
			if raise_exception:
				if not isinstance(ex, MindException):
					raise MindException(
						MindError(
							MindError.CODE_UNKNOWN,
							', '.join(ex.args),
							ex.args
						)
					)
				else:
					raise ex
			else:
				return False
		return True

	def unload_model(self, model_id)->bool:
		self.log().append('Unloading the model id: [{}]'.format(model_id))
		result = self.__drop_model(model_id)
		if result:
			self.log().append('The model id [{}] has been successfully unloaded'.format(model_id))
			self.model_list_check_sum_update()
		else:
			self.log().append('The model id [{}] has not been unloaded'.format(model_id))
		return result

	def __drop_model(self, model_id)->bool:
		del self.get_models()[model_id]
		return True

	def __load_models(self, a_tasks=None)->int:
		models_count = 0
		self.log().append('Loading models')
		tasks = a_tasks if a_tasks else self.get_tasks()
		if not tasks:
			self.log().append('Task list is empty')
			return models_count

		for task in tasks:
			if self.load_model(task):
				models_count += 1

		return models_count

	def is_model_exists(self, model_id: int) -> bool:
		return model_id in self.__models

	def get_models(self)->dict:
		return self.__models

	def get_model_list(self)->list:
		return list(self.__models.keys())

	def get_model(self, model_id: int):
		return self.__models.get(model_id, None)


def get_params_using_parser(args: list):
	params_parser = argparse.ArgumentParser()
	params_parser.add_argument(
		'-c', '--config_file',
		type=str, help='path to config file',
		default='configs/model_pool_config.json'
	)
	return params_parser.parse_args(args)


# --== Entry point ==--
if __name__ == "__main__":
	params = get_params_using_parser(sys.argv[1:])
	worker = ModelPool(**json.loads(FileHelper.get_text_file_content(params.config_file)))
	worker.run()
