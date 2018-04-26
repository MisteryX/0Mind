#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

import tornado
from tornado import ioloop, escape, httpclient
from abc import ABC, abstractmethod
from components.event_log import EventLog
import logging as log
import os
import psutil
import hashlib
import json


class Service(ABC):
	_id = None
	_host = None
	_port = None
	_tasks = None
	_options = None
	_server = None
	_event_log = None
	_model_list_hash = None
	_process = None
	_scheduler_tasks = []
	_pool_task_attributes = ['id', 'model_file', 'model_type', 'input_filters', 'output_filters']

	@abstractmethod
	def __init__(self, id, host, port, tasks, **options):
		self._id = id
		self._host = host
		self._port = port
		self._tasks = tasks
		self._options = options
		self._event_log = EventLog(name=self.get_name())
		self._process = psutil.Process(pid=os.getpid())
		self.get_process().cpu_percent()
		self.log().append('Initializing service on port {}'.format(self.get_port()))

	@abstractmethod
	def _init_service(self):
		raise NotImplementedError('you must to override this!')

	def _init_periodic_tasks(self):
		pass

	def get_option(self, name):
		return self._options.get(name, None)

	def get_options(self):
		return self._options

	@abstractmethod
	def get_model_list(self)->list:
		raise NotImplementedError('you must to override this!')

	@staticmethod
	def _is_dictionary_valid(dictionary: dict, attributes: list):
		for _attribute in attributes:
			if _attribute not in dictionary:
				return False, _attribute
		return True, None

	@staticmethod
	def _get_copy_of_dictionary_with_keys(dictionary: dict, keys: list) -> dict:
		return {key: dictionary[key] for key in keys if key in dictionary}

	@staticmethod
	def _get_list_of_values_from_list_of_dict(list_of_dict: list, key: str) -> list:
		result = []
		for dictionary in list_of_dict:
			value = dictionary.get(key)
			if value is not None:
				result.append(value)
		return result

	@staticmethod
	def _get_service_cpu_usage_url(service: dict):
		return 'http://{}:{}/info/system'.format(
			service.get('host'),
			service.get('port')
		)

	@staticmethod
	def _get_service_ping_url(service: dict) -> str:
		return 'http://{}:{}/info'.format(
			service.get('host'),
			service.get('port')
		)

	@staticmethod
	def _get_service_model_list_url(service: dict) -> str:
		return 'http://{}:{}/model/list'.format(
			service.get('host'),
			service.get('port')
		)

	@staticmethod
	def _get_response_from_url(request, http_client=None)->httpclient.HTTPResponse:
		if http_client is None or http_client:
			http_client = httpclient.HTTPClient()
		response = http_client.fetch(request)
		http_client.close()
		return response

	def _is_service_works(self, service: dict)->bool:
		try:
			response = self._get_response_from_url(self._get_service_ping_url(service))
			if response.error:
				self.log().append(
					'Ping of model pool id [{}] failed - {}: {}'.format(service.get('id'), response.code, response.body),
					log.ERROR
				)
				return False
			data = tornado.escape.json_decode(response.body)
			if 'id' not in data:
				self.log().append(
					'Ping of model pool id [{}]: result has no attribute [id]'.format(service.get('id')),
					log.ERROR
				)
				return False
			elif 'id' in data and data.get('id') != service.get('id'):
				self.log().append(
					'Ping of model pool id [{}]: service has returned [id] = {}'.format(service.get('id'), data.get('id')),
					log.ERROR
				)
				return False
			return True
		except Exception as ex:
			self.log().append(
				'Ping of model pool id [{}] failed: {}'.format(service.get('id'), str(ex.args)),
				log.ERROR
			)
			return False

	def get_id(self) -> int:
		return self._id

	def get_name(self):
		return self.__class__.__name__ + ':' + str(self.get_id())

	def get_tasks(self)->list:
		return self._tasks

	def append_task(self, task: dict):
		self._tasks.append(task)

	def remove_task(self, task_id: int)->int:
		removed_count = 0
		for __task in list(self._tasks):
			if __task['id'] == task_id:
				self._tasks.remove(__task)
				removed_count += 1
		return removed_count

	def pop_task(self, task_id: int)->dict:
		task = {}
		for __task in list(self._tasks):
			if __task['id'] == task_id:
				self._tasks.remove(__task)
				task = dict(__task)
		return task

	def get_pool_task_attributes(self)->list:
		return self._pool_task_attributes

	def get_port(self):
		return self._port

	def get_host(self):
		return self._host

	def get_server(self):
		return self._server

	def set_server(self, server):
		self._server = server

	def get_process(self):
		return self._process

	def get_current_cpu_usage(self):
		return self.get_process().cpu_percent()

	@staticmethod
	def get_memory_info() -> dict:
		return psutil.virtual_memory()._asdict()

	@staticmethod
	def calculate_model_list_check_sum(model_list: list)->str:
		hash_object = hashlib.md5()
		models = sorted(model_list)
		data = json.dumps(models).encode('utf-8')
		hash_object.update(data)
		return hash_object.hexdigest()

	def model_list_check_sum_update(self):
		self._model_list_hash = self.calculate_model_list_check_sum(self.get_model_list())

	def get_model_list_check_sum(self)->str:
		return self._model_list_hash

	def run(self):
		if self._scheduler_tasks:
			for task in self._scheduler_tasks:
				task.start()
			self.log().append('Run scheduled periodic tasks for {}'.format(self.__class__.__name__))

		if self._server:
			self.log().append('{} run on port {}'.format(self.__class__.__name__, self._port))
			tornado.ioloop.IOLoop.current().start()

	def stop(self):
		if self._scheduler_tasks:
			for task in self._scheduler_tasks:
				task.stop()
			self.log().append('Scheduled periodic tasks stopped for {}'.format(self.__class__.__name__))
		self.log().append('Stopping the server on port {}'.format(self._port))
		io_loop = tornado.ioloop.IOLoop.current()
		io_loop.add_callback(io_loop.stop)

	def log(self) -> EventLog:
		return self._event_log
