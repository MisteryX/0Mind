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


class CommandStopHandler(BaseHandler):
	_service = None
	_attributes = ['pool_id']

	async def post(self, *args, **kwargs):
		self._service.log().append('Received command [stop]')

		pool_id = int(self._data.get('pool_id', None)) if self._data else None
		if self._service.get_id() != pool_id:
			self._raise_error(500, 'Wrong pool_id={} for [stop] command'.format(pool_id))

		self.write({'result': 'accepted', 'id': pool_id})
		self._service.stop()

		self.finish()
