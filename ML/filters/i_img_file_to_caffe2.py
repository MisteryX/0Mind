#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.1"
__maintainer__ = "Maxim Morskov"
__site__ = "http://0mind.net"

from ML.filters.base_filter import BaseFilter
import numpy as np
import os
try:
	import skimage.io
	import skimage.transform
except ImportError as e:
	pass


class ImageFileCaffe2Filter(BaseFilter):

	def _apply(self):
		filtered_data = []
		if self.get_type() != 'input':
			self.get_model().set_error('filter',
				'{}: can be used only as an input filter'.format(self.__class__.__name__))
			return np.array(filtered_data)

		if type(self.get_data()) is not list or self.get_model().get_inputs()[self._input_output_id]['shape'][0] == 1:
			return np.array(self.get_filtered_image(self.get_data()[0]))

		for data_for_input in self.get_data():
			filtered_data.append(self.get_filtered_image(data_for_input))
		return np.array(filtered_data)

	def get_filtered_image(self, data_for_input: dict):
		if 'image_file' not in data_for_input:
			self.get_model().set_error('filter', '{}: image_file property missing'.format(self.__class__.__name__))
		return self.__get_images_cropped_and_scaled(data_for_input['image_file'])

	def __get_images_cropped_and_scaled(self, image_file_name: str):
		_input = self.get_model().get_inputs()[self._input_output_id]
		input_shape = list(filter(lambda item: item is not None, _input['shape']))
		target_channels = min(input_shape[1:])
		target_size = input_shape[-2:]
		if not os.path.isfile(image_file_name) or not os.access(image_file_name, os.R_OK):
			self.get_model().set_error('filter',
				'{}: file {} is not accessible'.format(self.__class__.__name__, image_file_name))
			return
		img = skimage.img_as_float(skimage.io.imread(image_file_name)).astype(np.float32)
		img = self.get_rescaled(img, target_size[0], target_size[1])
		img = self.crop_center(img, target_size[0], target_size[1])
		# switch to CHW
		img = img.swapaxes(1, 2).swapaxes(0, 1)
		# remove mean for better results
		img = img * 255 - 128
		# add batch size
		img = img[np.newaxis, :, :, :].astype(np.float32)
		return img

	@staticmethod
	def crop_center(img, cropx, cropy):
		y, x, c = img.shape
		startx = x // 2 - (cropx // 2)
		starty = y // 2 - (cropy // 2)
		return img[starty:starty + cropy, startx:startx + cropx]

	@staticmethod
	def get_rescaled(img, input_height, input_width):
		aspect = img.shape[1] / float(img.shape[0])
		if (aspect > 1):
			# landscape orientation - wide image
			res = int(aspect * input_height)
			imgScaled = skimage.transform.resize(img, (input_width, res))
		elif (aspect < 1):
			# portrait orientation - tall image
			res = int(input_width / aspect)
			imgScaled = skimage.transform.resize(img, (res, input_height))
		else: # (aspect == 1):
			imgScaled = skimage.transform.resize(img, (input_width, input_height))
		return imgScaled