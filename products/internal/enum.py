import random
from enum import Enum

from django.db import models


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

	def choices():
		return [(e.value, e.value) for e in GroupEnum]


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

	def choices():
		return [(e.value, e.value) for e in MaterialEnum]


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

	def choices():
		return [(e.value, e.value) for e in PlattingEnum]


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

	def choices():
		return [(e.value, e.value) for e in FinishEnum]


class StoneEnum(Enum):
	N                      = "None"
	AGATE                  = "Agate"
	AMAZONITE              = "Amazonite"
	AMETHYST               = "Amethyst"
	AQUAMARINE             = "Aquamarine"
	CALCITE                = "Calcite"
	CARNELIAN              = "Carnelian"
	CASSITERITE            = "Cassiterite"
	CHALCEDONY             = "Chalcedony"
	CHRYSOCOLLA            = "Chrysocolla"
	CHRYSOCOLLA_CHALCEDONY = "Chrysocolla Chalcedony"
	CORAL                  = "Coral"
	DIAMOND                = "Diamond"
	DOLOMITE               = "Dolomite"
	EMERALD                = "Emerald"
	HEMATITE               = "Hematite"
	JASPER                 = "Jasper"
	KYANITE                = "Kyanite"
	LABRADORITE            = "Labradorite"
	LAPIS_LAZULI           = "Lapis Lazuli"
	LAZULITE               = "Lazulite"
	MAGNESITE              = "Magnesite"
	MALACHITE              = "Malachite"
	MOONSTONE              = "Moonstone"
	ONYX                   = "Onyx"
	OPAL                   = "Opal"
	PEARL                  = "Pearl"
	QUARTZ                 = "Quartz"
	RHODONITE              = "Rhodonite"
	ROSE_QUARTZ            = "Rose Quartz"
	RUBY                   = "Ruby"
	SMOKY_QUARTZ           = "Smoky Quartz"
	SODALITE               = "Sodalite"
	TIGER_S_EYE            = "Tiger's Eye"
	TOPAZ                  = "Topaz"
	TOURMALINE             = "Tourmaline"
	TURQUOISE              = "Turquoise"
	ZIRCON                 = "Zircon"


	@staticmethod
	def str2Enum(s):
		for e in StoneEnum:
			if s == e.value:
				return e
		return StoneEnum.N

	def random():
		v = [e for e in StoneEnum]
		return random.choice(v)

	def choices():
		return [(e.value, e.value) for e in StoneEnum]


def createColor(name, hexValue):
	d = dict()
	d["name"]  = name
	d["value"] = hexValue

	return d

class ColorEnum(Enum):

	N                = createColor("None",             "#ffffff")

	BLACK            = createColor("Black",            "#000000")
	DARK_SLATE_GRAY  = createColor("Dark Slate Gray",  "#2F4F4F")
	SLATE_GRAY       = createColor("Slate Gray",       "#708090")
	GRAY             = createColor("Gray",             "#808080")

	SILVER           = createColor("Silver",           "#C0C0C0")
	IVORY            = createColor("Ivory",            "#FFFFF0")
	BEIGE            = createColor("Beige",            "#F5F5DC")
	WHITE            = createColor("White",            "#FFFFFF")
	DARK_RED         = createColor("Dark Red",         "#A52A2A")
	SADDLE_BROWN     = createColor("Saddle Brown",     "#8B4513")
	SIENNA           = createColor("Sienna",           "#A0522D")
	DARK_BLUE        = createColor("Dark Blue",        "#00008B")
	ROYAL_BLUE       = createColor("Royal Blue",       "#4169E1")
	LIGHT_SKY_BLUE   = createColor("Light Sky Blue",   "#87CEFA")
	CADET_BLUE       = createColor("Cadet Blue",       "#5F9EA0")
	TURQUOISE        = createColor("Turquoise",        "#40E0D0")
	AQUAMARINE       = createColor("Aquamarine",       "#7FFFD4")
	LIGHT_CYAN       = createColor("Light Cyan",       "#E0FFFF")
	TEAL             = createColor("Teal",             "#008080")
	LIGHT_SEA_GREEN  = createColor("Light Sea Green",  "#20B2AA")
	DARK_SEA_GREEN   = createColor("Dark Sea Green",   "#8FBC8B")
	DARK_OLIVE_GREEN = createColor("Dark Olive Green", "#556B2F")
	OLIVE            = createColor("Olive",            "#808000")
	DARK_GREEN       = createColor("Dark Green",       "#006400")
	GREEN            = createColor("Green",            "#008000")
	FOREST_GREEN     = createColor("Forest Green",     "#228B22")
	SEA_GREEN        = createColor("Sea Green",        "#2E8B57")
	EMERALD          = createColor("Emerald",          "#50C878")
	INDIGO           = createColor("Indigo",           "#4B0082")
	PURPLE           = createColor("Purple",           "#800080")
	DARK_VIOLET      = createColor("Dark Violet",      "#9400D3")
	DARK_KHAKI       = createColor("Dark Khaki",       "#BDB76B")
	GOLD             = createColor("Gold",             "#FFD700")
	YELLOW           = createColor("Yellow",           "#FFFF00")
	ORANGE           = createColor("Orange",           "#FFA500")
	DARK_ORANGE      = createColor("Dark Orange",      "#FF8C00")
	ORANGE_RED       = createColor("Orange Red",       "#FF4500")
	CORAL            = createColor("Coral",            "#FF7F50")
	LIGHT_SALMON     = createColor("Light Salmon",     "#FFA07A")
	PINK             = createColor("Pink",             "#FFC0CB")
	FIRE_BRICK       = createColor("Fire Brick",       "#B22222")
	RED              = createColor("Red",              "#FF0000")
	SALMON           = createColor("Salmon",           "#FA8072")
	INDIAN_RED       = createColor("Indian Red",       "#CD5C5C")


	@staticmethod
	def str2Enum(s):
		for e in ColorEnum:
			if s == e.value:
				return e
		return ColorEnum.N


	def random():
		v = [e for e in ColorEnum]
		return random.choice(v)


	def choices():
		return [(e.value, e.value['name']) for e in ColorEnum]
