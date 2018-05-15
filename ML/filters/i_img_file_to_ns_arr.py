#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

from ML.filters.base_filter import BaseFilter
from components.mind_exception import *
import numpy as np
import os
try:
	from PIL import Image
except Exception as ex:
	pass


class ImageFileToNormAndScaledNPArrayFilter(BaseFilter):

	def _apply(self):
		filtered_data = []
		if self.get_type() != 'input':
			self.get_model().set_error(MindError(
				ERROR_CODE_FILTER_WRONG_TYPE,
				'{}: can be used only as an input filter',
				[self.__class__.__name__]
			))
			return np.array(filtered_data)
		for data_for_input in self.get_data():
			if 'image_file' in data_for_input:
				filtered_data.append(
					self.__get_images_norm_and_scaled(data_for_input['image_file']))
			else:
				self.get_model().set_error(MindError(
					ERROR_CODE_FILTER_WRONG_PARAMS,
					'{}: missing param [{}]',
					[self.__class__.__name__, 'image_file']
				))
		return np.array(filtered_data)

	def __get_images_norm_and_scaled(self, image_file_name: str):
		_input = self.get_model().get_inputs()[self._input_output_id]
		input_shape = list(filter(lambda item: item is not None, _input['shape']))
		target_channels = min(input_shape[1:])
		target_size = tuple(list(filter(lambda item: item != target_channels, input_shape)))
		if not os.path.isfile(image_file_name) or not os.access(image_file_name, os.R_OK):
			self.get_model().set_error(MindError(
				ERROR_CODE_FILTER_FILE_IS_UNREACHABLE,
				'{}: file [{}] is not accessible',
				[self.__class__.__name__, image_file_name]
			))
			return
		_image = Image.open(image_file_name)
		_image = _image.resize(target_size, Image.ANTIALIAS)
		_image = _image.convert(mode=self.__get_pillow_mode_for_channels(target_channels))
		result = np.asarray(_image, dtype=_input['type'])
		result /= 255  # normalization
		result = result.reshape(input_shape)
		return result

	@staticmethod
	def __get_pillow_mode_for_channels(channels_number: int):
		map = {
			1: 'L',
			3: 'RGB',
			4: 'RGBA'
		}
		if channels_number in map:
			return map[channels_number]
		return 'RGB'