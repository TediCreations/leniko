import os
import random

from django.core.exceptions import FieldDoesNotExist
from django.core.exceptions import ValidationError
from django.db import models

from sorl.thumbnail.base import ThumbnailBackend
from sorl.thumbnail.base import EXTENSIONS

from enum import Enum
from itertools import chain


class AbstractModel(models.Model):

	"""Abstract class for Models"""

	@classmethod
	def create(cls, dictionary):
		"""Create a new instance of the model"""

		className = cls.__name__
		if not isinstance(dictionary, dict):
			raise Exception(f"Needs a dictionary to create {className}")

		# Sanitize the dictionary
		sanitizedDictionary = dict()
		for key, value in dictionary.items():
			try:
				cls._meta.get_field(key)
				sanitizedDictionary[key] = value
			except FieldDoesNotExist:
				pass

		# Create instance
		obj = None
		try:
			obj = cls(**sanitizedDictionary)
		except TypeError:
			raise Exception("Could not create {className}")

		# Validate
		try:
			obj.clean()
		except ValidationError:
			raise

		# Return record of instance
		return obj

	def to_txt(self, indent=0):
		"""Provide a string for pretty print of the model's fields"""
		d = self.to_dict()
		indent = 0
		txt = f"\033[91m{self.__class__.__name__}\033[0m\r\n"
		for key, value in d.items():
			txt += '\t' * indent + "\033[93m" + str(key) + "\033[0m:"
			if isinstance(value, dict):
				txt += self.to_txt(value, indent + 1)
			else:
				if isinstance(value, Enum):
					value = value.value
				txt += ('\t' * (indent + 1) + str(value)) + "\r\n"
		return txt

	def getRandomObject(self):
		objList = type(self).objects.all()
		obj = random.choice(objList)
		return obj

	def to_dict(self):
		"""Automatically get all the model's field keys and values in a dictionary"""

		# For the parent
		parentData = dict()
		try:
			parentData = super().to_dict()
		except AttributeError:
			pass

		# For this instance
		opts = self._meta
		data = {}
		for f in chain(opts.concrete_fields, opts.private_fields):
			data[f.name] = f.value_from_object(self)
		for f in opts.many_to_many:
			data[f.name] = [i.id for i in f.value_from_object(self)]

		# TODO: Order od dictionary merge
		# return {**parentData, **data}
		return {**data, **parentData}

	class Meta:
		abstract = True


class MyThumbnailBackend(ThumbnailBackend):

	def _get_thumbnail_filename(self, *args, **kwargs):

		filepath = str(args[0])
		dirname = os.path.dirname(filepath)
		name = os.path.splitext(os.path.basename(filepath))[0]

		# New attributes
		geometry = args[1]
		crop = args[2]['crop']
		quality = args[2]['quality']
		newSuffix = EXTENSIONS[args[2]['format']]
		colorspace = args[2]['colorspace']
		quality = args[2]['quality']
		padding = args[2]['padding']

		# Default attributes
		default_colorspace = ThumbnailBackend.default_options['colorspace']

		# Compute the new filepath
		filepath = f"{dirname}/{name}"

		if crop:
			filepath += "_C"
		if quality != 100:
			filepath += f"_Q{quality}"
		if default_colorspace != colorspace:
			filepath += f"_S{colorspace}"
		if padding:
			filepath += "_P"

		filepath += f"_{geometry}.{newSuffix}"
		filepath = os.path.join("cache/", filepath)

		return filepath
