import random
from enum import Enum

from django.db import models
from django_enum_choices.fields import EnumChoiceField


class GroupEnum(Enum):
	N  = "Not in group"
	BR = "Bracelet"
	NE = "Necklace"
	RI = "Ring"
	EA = "Earring"

	@staticmethod
	def str2Enum(s):
		for e in GroupEnum:
			if s == e.value:
				return e
		return GroupEnum.N

	def random():
		v = [e for e in GroupEnum]
		return random.choice(v)


class MaterialEnum(Enum):
	N    = "None"
	BR   = "Bronze"
	SI   = "Silver 925°"
	GO14 = "Gold 14K"
	GO25 = "Gold 25K"

	@staticmethod
	def str2Enum(s):
		for e in MaterialEnum:
			if s == e.value:
				return e
		return MaterialEnum.N

	def random():
		v = [e for e in MaterialEnum]
		return random.choice(v)


class PlattingEnum(Enum):
	N  = "Not platted"
	SI = "Silver"
	GO = "Gold"

	@staticmethod
	def str2Enum(s):
		for e in PlattingEnum:
			if s == e.value:
				return e
		return PlattingEnum.N

	def random():
		v = [e for e in PlattingEnum]
		return random.choice(v)


class FinishEnum(Enum):
	N = "None"
	M = "Matte"
	B = "Bright"

	@staticmethod
	def str2Enum(s):
		for e in FinishEnum:
			if s == e.value:
				return e
		return FinishEnum.N

	def random():
		v = [e for e in FinishEnum]
		return random.choice(v)


class StoneEnum(Enum):
	N  = "None"
	AG = "Agate"
	LL = "Lapis Lazulis"
	AM = "Amethyst"
	AV = "Aventurine"
	CA = "Carnelian"
	CO = "Coral"
	EM = "Emerald"

	@staticmethod
	def str2Enum(s):
		for e in StoneEnum:
			if s == e.value:
				return e
		return StoneEnum.N

	def random():
		v = [e for e in StoneEnum]
		return random.choice(v)


class ColorEnum(Enum):
	N  = "None"
	RED  = "Red"
	YEL  = "Yellow"
	GRE  = "Green"
	BLU  = "Blue"
	WHI  = "White"
	BLA  = "Black"
	SIL  = "Silver"

	@staticmethod
	def str2Enum(s):
		for e in ColorEnum:
			if s == e.value:
				return e
		return ColorEnum.N

	def random():
            v = [e for e in ColorEnum]
            return random.choice(v)
