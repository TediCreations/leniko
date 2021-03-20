import random
from enum import Enum


class GroupEnum(Enum):
	N = "Not in group"
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


def createMaterial(id, name):
	d = dict()
	d["id"] = id
	d["name"] = name

	return d


class MaterialEnum(Enum):
	N = createMaterial("NO", "None")
	BR = createMaterial("BR", "Brass")
	SI = createMaterial("SI", "Silver 925")
	GO14 = createMaterial("14", "Gold 14K")
	GO25 = createMaterial("25", "Gold 25K")

	def getId(self):
		n = self.value['id']
		return n

	def getName(self):
		name = self.value['name']
		return name

	@staticmethod
	def str2Enum(s):
		for e in MaterialEnum:
			if s == e.value['name']:
				return e
		return MaterialEnum.N

	def random():
		v = [e for e in MaterialEnum]
		return random.choice(v)

	def choices():
		return [(e.value, e.value['name']) for e in MaterialEnum]


class PlattingEnum(Enum):
	N = "Not platted"
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


def createStone(id, name):
	d = dict()
	d["id"] = id
	d["name"] = name

	return d


class StoneEnum(Enum):
	N                      = createStone(0,  "None")
	AGATE                  = createStone(1,  "Agate")
	AMAZONITE              = createStone(2,  "Amazonite")
	AMETHYST               = createStone(3,  "Amethyst")
	AQUAMARINE             = createStone(4,  "Aquamarine")
	CALCITE                = createStone(5,  "Calcite")
	CARNELIAN              = createStone(6,  "Carnelian")
	CASSITERITE            = createStone(7,  "Cassiterite")
	CHALCEDONY             = createStone(8,  "Chalcedony")
	CHRYSOCOLLA            = createStone(9,  "Chrysocolla")
	CHRYSOCOLLA_CHALCEDONY = createStone(10, "Chrysocolla Chalcedony")
	CORAL                  = createStone(11, "Coral")
	DIAMOND                = createStone(12, "Diamond")
	DOLOMITE               = createStone(13, "Dolomite")
	EMERALD                = createStone(14, "Emerald")
	HEMATITE               = createStone(15, "Hematite")
	JASPER                 = createStone(16, "Jasper")
	KYANITE                = createStone(17, "Kyanite")
	LABRADORITE            = createStone(18, "Labradorite")
	LAPIS_LAZULI           = createStone(19, "Lapis Lazuli")
	LAZULITE               = createStone(20, "Lazulite")
	MAGNESITE              = createStone(21, "Magnesite")
	MALACHITE              = createStone(22, "Malachite")
	MOONSTONE              = createStone(23, "Moonstone")
	ONYX                   = createStone(24, "Onyx")
	OPAL                   = createStone(25, "Opal")
	PEARL                  = createStone(26, "Pearl")
	QUARTZ                 = createStone(27, "Quartz")
	RHODONITE              = createStone(28, "Rhodonite")
	ROSE_QUARTZ            = createStone(29, "Rose Quartz")
	RUBY                   = createStone(30, "Ruby")
	SMOKY_QUARTZ           = createStone(31, "Smoky Quartz")
	SODALITE               = createStone(32, "Sodalite")
	TIGER_S_EYE            = createStone(33, "Tiger's Eye")
	TOPAZ                  = createStone(34, "Topaz")
	TOURMALINE             = createStone(35, "Tourmaline")
	TURQUOISE              = createStone(36, "Turquoise")
	ZIRCON                 = createStone(37, "Zircon")

	def getId(self):
		n = self.value['id']
		return f"{n:02d}"

	def getName(self):
		name = self.value['name']
		return name

	@staticmethod
	def str2Enum(s):
		for e in StoneEnum:
			if s == e.value['name']:
				return e
		return StoneEnum.N

	def random():
		v = [e for e in StoneEnum]
		return random.choice(v)

	def choices():
		return [(e.value, e.value['name']) for e in StoneEnum]


def createColor(id, name, hexValue):
	d = dict()
	d["id"] = id
	d["name"] = name
	d["value"] = hexValue

	return d


class ColorEnum(Enum):

	N                = createColor(0,  "None",             "#ffffff")

	BLACK            = createColor(1,  "Black",            "#000000")
	DARK_SLATE_GRAY  = createColor(2,  "Dark Slate Gray",  "#2F4F4F")
	SLATE_GRAY       = createColor(3,  "Slate Gray",       "#708090")
	GRAY             = createColor(4,  "Gray",             "#808080")

	SILVER           = createColor(5,  "Silver",           "#C0C0C0")
	IVORY            = createColor(6,  "Ivory",            "#FFFFF0")
	BEIGE            = createColor(7,  "Beige",            "#F5F5DC")
	WHITE            = createColor(8,  "White",            "#FFFFFF")
	DARK_RED         = createColor(9,  "Dark Red",         "#A52A2A")
	SADDLE_BROWN     = createColor(10, "Saddle Brown",     "#8B4513")
	SIENNA           = createColor(11, "Sienna",           "#A0522D")
	DARK_BLUE        = createColor(12, "Dark Blue",        "#00008B")
	ROYAL_BLUE       = createColor(13, "Blue Royal",       "#4169E1")
	LIGHT_SKY_BLUE   = createColor(14, "Light Sky Blue",   "#87CEFA")
	CADET_BLUE       = createColor(15, "Cadet Blue",       "#5F9EA0")
	TURQUOISE        = createColor(16, "Turquoise",        "#40E0D0")
	AQUAMARINE       = createColor(17, "Aquamarine",       "#7FFFD4")
	LIGHT_CYAN       = createColor(18, "Light Cyan",       "#E0FFFF")
	TEAL             = createColor(19, "Teal",             "#008080")
	LIGHT_SEA_GREEN  = createColor(20, "Light Sea Green",  "#20B2AA")
	DARK_SEA_GREEN   = createColor(21, "Dark Sea Green",   "#8FBC8B")
	DARK_OLIVE_GREEN = createColor(22, "Dark Olive Green", "#556B2F")
	OLIVE            = createColor(23, "Olive",            "#808000")
	DARK_GREEN       = createColor(24, "Dark Green",       "#006400")
	GREEN            = createColor(25, "Green",            "#008000")
	FOREST_GREEN     = createColor(26, "Forest Green",     "#228B22")
	SEA_GREEN        = createColor(27, "Sea Green",        "#2E8B57")
	EMERALD          = createColor(28, "Emerald",          "#50C878")
	INDIGO           = createColor(29, "Indigo",           "#4B0082")
	PURPLE           = createColor(30, "Purple",           "#800080")
	DARK_VIOLET      = createColor(31, "Dark Violet",      "#9400D3")
	DARK_KHAKI       = createColor(32, "Dark Khaki",       "#BDB76B")
	GOLD             = createColor(33, "Gold",             "#FFD700")
	YELLOW           = createColor(34, "Yellow",           "#FFFF00")
	ORANGE           = createColor(35, "Orange",           "#FFA500")
	DARK_ORANGE      = createColor(36, "Dark Orange",      "#FF8C00")
	ORANGE_RED       = createColor(37, "Orange Red",       "#FF4500")
	CORAL            = createColor(38, "Coral",            "#FF7F50")
	LIGHT_SALMON     = createColor(39, "Light Salmon",     "#FFA07A")
	PINK             = createColor(40, "Pink",             "#FFC0CB")
	BORDEAUX         = createColor(41, "Bordeaux",         "#B22222")
	RED              = createColor(42, "Red",              "#FF0000")
	SALMON           = createColor(43, "Salmon",           "#FA8072")
	INDIAN_RED       = createColor(44, "Indian Red",       "#CD5C5C")
	BLUE_RAF         = createColor(45, "Blue Raf",         "#20639B")

	def getId(self):
		n = self.value['id']
		return f"{n:02d}"

	def getName(self):
		name = self.value['name']
		return name

	@staticmethod
	def str2Enum(s):
		for e in ColorEnum:
			if s == e.value['name']:
				return e
		return ColorEnum.N

	def random():
		v = [e for e in ColorEnum]
		return random.choice(v)

	def choices():
		return [(e.value, e.value['name']) for e in ColorEnum]
