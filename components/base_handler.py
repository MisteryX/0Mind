#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.1"
__maintainer__ = "Maxim Morskov"
__site__ = "http://0mind.net"

import tornado
from tornado import web, escape, httpclient, gen
import logging as log


SLEEP_PERIOD_UNTIL_NEXT_TRY = 0.002


class BaseHandler(tornado.web.RequestHandler):
	_service = None
	_json_attributes = []
	_data = None

	def initialize(self, service):
		self._service = service
		self.set_header('Server', '0Mind')

	def prepare(self):
		if self.request.body:
			content_type = self.request.headers.get('content-type', '')
			if content_type != 'application/json':
				self._raise_error(400, '{}: Wrong header Content-Type: {}'.format(self.__class__.__name__, content_type))
			self._data = tornado.escape.json_decode(self.request.body)
			self._validate_data(self._data, self._json_attributes)

	def on_finish(self):
		pass

	def _validate_data(self, data: dict, expected_attributes: list, container_type='JSON'):
		for attribute in expected_attributes:
			if attribute not in data:
				self._raise_error(
					400,
					'{}: Wrong request! Missing compulsory {} attribute [{}]'.format(self.__class__.__name__, container_type, attribute)
				)

	def _raise_error(self, http_code: int, message: str):
		self._service.log().append('ERROR', message, log.ERROR)
		self.set_status(http_code)
		self.write({'error': message})
		self.finish()

	'''
	@return Service
	'''
	def get_service(self):
		return self._service

	def get_data(self):
		return self._data

	@staticmethod
	def get_response_from_url_async(http_request: tornado.httpclient.HTTPRequest, response_handler=None, http_client=None):
		if http_client is None:
			http_client = tornado.httpclient.AsyncHTTPClient()
		return http_client.fetch(http_request, callback=response_handler, raise_error=False)

	@staticmethod
	async def _wait_until_all_tasks_finished(task_list: list):
		while task_list:
			await gen.sleep(SLEEP_PERIOD_UNTIL_NEXT_TRY)
			for _task in list(task_list):
				if _task.done:
					task_list.remove(_task)
