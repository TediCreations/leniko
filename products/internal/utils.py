import random

from django.core.exceptions import FieldDoesNotExist
from django.db              import models

from enum        import Enum
from itertools   import chain



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
		indent=0
		txt = f"\033[91m{self.__class__.__name__}\033[0m\r\n"
		for key, value in d.items():
			txt += '\t' * indent + "\033[93m" + str(key) + "\033[0m:"
			if isinstance(value, dict):
				txt += self.to_txt(value, indent+1)
			else:
				if isinstance(value, Enum):
					value = value.value
				txt +=('\t' * (indent+1) + str(value)) + "\r\n"
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
		#return {**parentData, **data}
		return {**data, **parentData}

	class Meta:
		abstract = True
