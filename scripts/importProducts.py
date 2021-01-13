import os
import shutil

from products.internal.enum import GroupEnum
from products.internal.enum import MaterialEnum
from products.internal.enum import PlattingEnum
from products.internal.enum import StoneEnum
from products.internal.enum import ColorEnum

from products.models        import Product
from products.models        import Jewelry
from products.models        import JewelryGroup
from products.models        import JewelryPhoto
from products.models        import Bracelet
from products.models        import Necklace
from products.models        import Ring
from products.models        import Earring

from products.models        import ProductTool


def str2Bool(s):
	value = s.lower()
	if not value in ("true", "false", "yes", "no"):
		raise Exception("{s} is not a valid string that respesents a boolean type")
	return value in ("true", "yes")


def str2float(s):
	return float(s)


def readCommonTxt(path, d):
	filepath = os.path.join(path, "common.txt")
	try:
		f = open(filepath, "r")
		lines = f.readlines()
		f.close()
	except Exception:
		print(f"ERROR while opening, writing {filepath}")
		exit()
	for line in lines:
		line = line.strip()
		if line == "":
			continue
		data = line.split(":")
		if len(data) != 2:
			raise Exception(f"Failed to parse '{filepath}'")
		key   = data[0]
		value = data[1].strip()

		if key == "brief":
			d['brief'] = str(value)
		elif key == "description":
			d['description'] = str(value)
		elif key == "stone":
			d['stone'] = StoneEnum.str2Enum(value)
		elif key == "macrame":
			d['macrame'] = str2Bool(value)
		elif key == "pcolor":
			d['pcolor'] = ColorEnum.str2Enum(value)
		else:
			raise Exception(f"Invalid key '{key}' for '{filepath}'")

	return d


def readGroupTxt(path, d):
	group = d["group"].value
	filepath = os.path.join(path, f"{group}.txt")
	try:
		f = open(filepath, "r")
		lines = f.readlines()
		f.close()
	except Exception:
		print(f"ERROR while opening, writing {filepath}")
		exit()
	for line in lines:
		line = line.strip()
		if line == "":
			continue
		data = line.split(":")
		if len(data) != 2:
			raise Exception(f"Failed to parse '{filepath}'")
		key   = data[0]
		value = data[1].strip()

		# Bracelet
		if group == "Bracelet":
			if key == "diameter_max":
				d['diameter_max'] = value
			elif key == "diameter_min":
				d['diameter_min'] = value
			elif key == "width_max":
				d['width_max'] = value
			elif key == "width_min":
				d['width_min'] = value
			elif key == "isAdjustable":
				d['isAdjustable'] = str2Bool(value)
			else:
				raise Exception(f"Invalid key '{key}' for '{filepath}'")
		elif group == "Necklace":
			if key == "length":
				d['length'] = value
			elif key == "width_max":
				d['width_max'] = value
			elif key == "width_min":
				d['width_min'] = value
			elif key == "isAdjustable":
				d['isAdjustable'] = str2Bool(value)
			else:
				raise Exception(f"Invalid key '{key}' for '{filepath}'")
		elif group == "Ring":
			if key == "circumference":
				d['circumference'] = value
			elif key == "width_max":
				d['width_max'] = value
			elif key == "width_min":
				d['width_min'] = value
			elif key == "isAdjustable":
				d['isAdjustable'] = str2Bool(value)
			else:
				raise Exception(f"Invalid key '{key}' for '{filepath}'")
		elif group == "Earring":
			if key == "heigth":
				d['heigth'] = value
			elif key == "width_max":
				d['width_max'] = value
			elif key == "width_min":
				d['width_min'] = value
			else:
				raise Exception(f"Invalid key '{key}' for '{filepath}'")
		else:
			raise Exception(f"Invalid group for '{filepath}'")

	return d


def readInfoTxt(path, d):
	filepath = os.path.join(path, "info.txt")
	f = open(filepath, "r")
	lines = f.readlines()
	f.close()
	for line in lines:
		line = line.strip()
		if line == "":
			continue
		data = line.split(":")
		if len(data) != 2:
			raise Exception(f"Failed to parse '{filepath}'")
		key   = data[0]
		value = data[1].strip()

		if key == "material":
			d['material'] = MaterialEnum.str2Enum(value)
		elif key == "platting":
			d['platting'] = PlattingEnum.str2Enum(value)
		elif key == "scolor":
			d['scolor'] = ColorEnum.str2Enum(value)
		else:
			raise Exception(f"Invalid key '{key}' for '{filepath}'")

	return d


def readProductTxt(path, d):
	filepath = os.path.join(path, "product.txt")
	f = open(filepath, "r")
	lines = f.readlines()
	f.close()
	for line in lines:
		line = line.strip()
		if line == "":
			continue
		data = line.split(":")
		if len(data) != 2:
			raise Exception(f"Failed to parse '{filepath}'")
		key   = data[0]
		value = data[1].strip()

		if key == "Price":
			d['price'] = value
		elif key == "isFeatured":
			d['isFeatured'] = str2Bool(value)
		elif key == "isActive":
			d['isActive'] = str2Bool(value)
		else:
			raise Exception(f"Invalid key '{key}' for '{filepath}'")

	return d


def fprint(f):
	#print(f)
	pass


def importData(sourceDir):

	if not isinstance(sourceDir, str):
		print(f"Please give a valid directory path")
		exit()

	if not os.path.isdir(sourceDir):
		print(f"{sourceDir} is missing")
		exit()

	path = sourceDir
	groups = [f for f in os.listdir(path) if not os.path.isfile(os.path.join(path, f))]
	for group in groups:
		fprint("#####################################################")
		fprint(f"Group:         {group}")

		# Gather info
		d = dict()
		d['sku']         = None
		d['price']       = None
		d['isFeatured']  = None
		d['isActive']    = None

		d['title']       = None
		d['group']       = GroupEnum.str2Enum(group)
		d['brief']       = None
		d['description'] = None
		d['stone']       = None
		d['macrame']     = None
		d['pcolor']      = None # Primary

		d['material']    = None
		d['platting']    = None
		d['scolor']      = None # Secondary

		d['photos']      = None

		path = os.path.join(sourceDir, group)
		jewelrys = os.listdir(path)
		for jewelry in jewelrys:
			fprint(f"-----------------------------------------------------")
			fprint(f"Jewelry:       {jewelry}")

			# The directory name is the name of the jewelry
			d['title'] = jewelry

			path = os.path.join(sourceDir, group, jewelry)
			variationFiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
			for variationFile in variationFiles:
				if variationFile == "common.txt":
					d = readCommonTxt(path, d)
				elif variationFile == f"{group}.txt":
					d = readGroupTxt(path, d)
				else:
					fprint(f"VariationFile: {variationFile}")

			variationDirs  = [f for f in os.listdir(path) if not os.path.isfile(os.path.join(path, f))]
			for variationDir in variationDirs:
				fprint(f"VariationDir:  {variationDir}")

				path = os.path.join(sourceDir, group, jewelry, variationDir)
				files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
				photoList = list()
				for file in files:
					if file == "info.txt":
						isInfoFileAvailable = True
						d = readInfoTxt(path, d)
					elif file == "product.txt":
						isProductFileAvailable = True
						d = readProductTxt(path, d)
					else:
						fprint(f"File:          {file}")
						photoPath = os.path.join(path, file)
						photoList.append(photoPath)

				d["photos"] = photoList

				ProductTool.create(d)

		fprint("\r\n")
