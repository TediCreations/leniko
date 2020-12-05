#!/usr/bin/env python3

import os
import random

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leniko.settings")
django.setup()


from products.models     import Product
from products.models     import Jewelry
from products.models     import JewelryGroup
from products.models     import JewelryPhoto
from products.models     import JewelryColor
from products.models     import Bracelet
from products.models     import Necklace
from products.models     import Ring
from products.models     import Earring

from products.models     import ProductTool

from products.internal.enum import StoneEnum
from products.internal.enum import ColorEnum
from products.internal.enum import MaterialEnum
from products.internal.enum import PlattingEnum
from products.internal.enum import GroupEnum


#def test(self, indent=0):
#	print(f"Self:      {self}")
#	print(f"Meta:      {self._meta}")
#	print(f"Type self: {type(self)}")
#	print(f"Type meta: {type(self._meta)}")
#	print(f"Concrete:  {self._meta.concrete_fields}")
#	print(f"Private:   {self._meta.private_fields}")
#	pass


def registerJewelryVariation():
	def random_line(fname):
		lines = open(fname).read().splitlines()
		return random.choice(lines)

	def random_bool():
		return not random.getrandbits(1)

	def random_price():
		return round(random.uniform(5, 999), 2)

	def getRandomPhotoList(static_dir):
		n = int(random.uniform(0, 9))
		photoList = list()
		for i in range(n):
			url = random.choice([x for x in os.listdir(static_dir) if os.path.isfile(os.path.join(static_dir, x))])
			baseUrl = os.path.join(static_dir, url)
			photoList.append(baseUrl)
		return photoList

	def getRandomColorList():
		n = int(random.uniform(0, 5))
		colorList = list()
		for i in range(n):
			color = ColorEnum.random()
			colorList.append(color)
		return colorList


	dictionary = dict()

	# Product
	#dictionary["sku"]          = "?"
	dictionary["price"]         = random_price()
	dictionary["isFeatured"]    = random_bool()
	dictionary["isActive"]      = random_bool()

	# Jewelry Common
	dictionary["title"]         = random_line('tests/products/titleList')
	dictionary["brief"]         = random_line('tests/products/briefList')
	dictionary["description"]   = "Default description..."
	dictionary["stone"]         = StoneEnum.random()
	dictionary["macrame"]       = random_bool()
	dictionary["color"]         = ColorEnum.random()

	# Jewelry Variation
	dictionary["material"]     = MaterialEnum.random()
	dictionary["platting"]     = PlattingEnum.random()
	dictionary["group"]        = GroupEnum.random()

	dictionary["heigth"]        = int(random.uniform(0, 999))
	dictionary["length"]        = int(random.uniform(0, 999))
	dictionary["circumference"] = int(random.uniform(0, 999))
	dictionary["width_max"]     = int(random.uniform(0, 999))
	dictionary["width_min"]     = int(random.uniform(0, 999))
	dictionary["diameter_max"]  = int(random.uniform(0, 999))
	dictionary["diameter_min"]  = int(random.uniform(0, 999))
	dictionary["isAdjustable"]  = random_bool()

	dictionary["photos"]        = getRandomPhotoList("static/img/jewel/")
	dictionary["colors"]        = getRandomColorList()

	# Invalid
	dictionary["invalid"]       = "Invalid dictionary keys are ignored!"

	# Do not let Group to be None
	if dictionary["group"] is GroupEnum.N:
		print("Group is None")
		return

	ProductTool.create(dictionary)
	print("Done")


	#tablelist = (Product, Jewelry, JewelryGroup, JewelryPhoto, JewelryColor, Bracelet, Necklace, Ring, Earring)
	#method_list = dir(Fuck)
	#method_list = [func for func in dir(Fuck) if callable(getattr(Fuck, func)) and not func.startswith("__")]
	#for m in method_list:
	#	#print(m)
	#	pass


def main():
	for i in range(100):
		print("---------------------")
		registerJewelryVariation()


if __name__ == "__main__":
	main()
