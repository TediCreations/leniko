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


class ColorEnum(Enum):

	N                = "None"
	BLACK            = "Black"            #000000
	DARK_SLATE_GRAY  = "Dark Slate Gray"  #2F4F4F
	SLATE_GRAY       = "Slate Gray"       #708090
	GRAY             = "Gray"             #808080
	SILVER           = "Silver"           #C0C0C0
	IVORY            = "Ivory"            #FFFFF0
	BEIGE            = "Beige"            #F5F5DC
	WHITE            = "White"            #FFFFFF
	DARK_RED         = "Dark Red"         #A52A2A
	SADDLE_BROWN     = "Saddle Brown"     #8B4513
	SIENNA           = "Sienna"           #A0522D
	DARK_BLUE        = "Dark Blue"        #00008B
	ROYAL_BLUE       = "Royal Blue"       #4169E1
	LIGHT_SKY_BLUE   = "Light Sky Blue"   #87CEFA
	CADET_BLUE       = "Cadet Blue"       #5F9EA0
	TURQUOISE        = "Turquoise"        #40E0D0
	AQUAMARINE       = "Aquamarine"       #7FFFD4
	LIGHT_CYAN       = "Light Cyan"       #E0FFFF
	TEAL             = "Teal"             #008080
	LIGHT_SEA_GREEN  = "Light Sea Green"  #20B2AA
	DARK_SEA_GREEN   = "Dark Sea Green"   #8FBC8B
	DARK_OLIVE_GREEN = "Dark Olive Green" #556B2F
	OLIVE            = "Olive"            #808000
	DARK_GREEN       = "Dark Green"       #006400
	GREEN            = "Green"            #008000
	FOREST_GREEN     = "Forest Green"     #228B22
	SEA_GREEN        = "Sea Green"        #2E8B57
	EMERALD          = "Emerald"          #50C878
	INDIGO           = "Indigo"           #4B0082
	PURPLE           = "Purple"           #800080
	DARK_VIOLET      = "Dark Violet"      #9400D3
	DARK_KHAKI       = "Dark Khaki"       #BDB76B
	GOLD             = "Gold"             #FFD700
	YELLOW           = "Yellow"           #FFFF00
	ORANGE           = "Orange"           #FFA500
	DARK_ORANGE      = "Dark Orange"      #FF8C00
	ORANGE_RED       = "Orange Red"       #FF4500
	CORAL            = "Coral"            #FF7F50
	LIGHT_SALMON     = "Light Salmon"     #FFA07A
	PINK             = "Pink"             #FFC0CB
	FIRE_BRICK       = "Fire Brick"       #B22222
	RED              = "Red"              #FF0000
	SALMON           = "Salmon"           #FA8072
	INDIAN_RED       = "Indian Red"       #CD5C5C


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
		return [(e.value, e.value) for e in ColorEnum]
