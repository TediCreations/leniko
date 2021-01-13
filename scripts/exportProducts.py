#!/usr/bin/env python3

import os
import errno
import shutil

from django.conf import settings

from products.internal.enum import ColorEnum

from products.models        import Product
from products.models        import Jewelry
from products.models        import JewelryGroup
from products.models        import JewelryPhoto
from products.models        import Bracelet
from products.models        import Necklace
from products.models        import Ring
from products.models        import Earring


def bool2YesNo(b):
	b = str(b).lower()
	if b not in ("true", "false"):
		raise Exception("Could not translate string boolean to yes/no")
	if b == "true":
		return "Yes"
	else:
		return "No"

def exportData(baseDirPath):

	if not isinstance(baseDirPath, str):
		print("Please give a valid directory path")
		exit()

	#-----------------------------------------------------------------------
	# Queries
	products = Product.objects.all()
	productLen = len(products)
	print(f"Products:      {productLen}")

	jewelrys = Jewelry.objects.all()
	jewelrysLen = len(jewelrys)
	print(f"Jewelrys:      {jewelrysLen}")

	jewelryGroups = JewelryGroup.objects.all()
	jewelryGroupsLen = len(jewelryGroups)
	print(f"JewelryGroups: {jewelryGroupsLen}")

	bracelets = Bracelet.objects.all()
	braceletsLen = len(bracelets)
	print(f"Bracelets:     {braceletsLen}")

	necklaces = Necklace.objects.all()
	necklacesLen = len(necklaces)
	print(f"Necklaces:     {necklacesLen}")

	rings = Ring.objects.all()
	ringsLen = len(rings)
	print(f"Rings:         {ringsLen}")

	earrings = Earring.objects.all()
	earringsLen = len(earrings)
	print(f"Earrings:      {earringsLen}")

	#-----------------------------------------------------------------------
	# Delete directory
	try:
		shutil.rmtree(baseDirPath)
	except FileNotFoundError:
		pass

	# Create directory
	if not os.path.isdir(baseDirPath):
		try:
			os.mkdir(baseDirPath)
		except OSError:
			messages.add_message(request, messages.ERROR, f"Creation of the directory '{baseDirPath}' failed.")
			return
	else:
		messages.add_message(request, messages.ERROR, f"Deletion of directory '{baseDirPath}' failed.")

	# Export
	# For each product in the query
	for product in products:

		# Gather info
		d = dict()
		d['sku']         = product.sku
		d['price']       = product.price

		d['isFeatured']  = product.isFeatured
		d['isActive']    = product.isActive

		d['title']       = product.jewelry.getTitle()
		d['group']       = product.jewelry.getGroup()
		d['brief']       = product.jewelry.getBrief()
		d['description'] = product.jewelry.getDescription()
		d['stone']       = product.jewelry.getStone().getName()
		d['macrame']     = product.jewelry.getMacrame()
		d['pcolor']      = product.jewelry.getPrimaryColor().getName() # Primary

		d['material']    = product.jewelry.getMaterial().getName()
		d['platting']    = product.jewelry.getPlatting()
		d['scolor']      = product.jewelry.getSecondaryColor().getName() # Secondary

		d['photos']      = list()

		i = 1
		variationNumber = None
		for variation in Jewelry.objects.filter(group=product.jewelry.group):
			# Check variation
			if variation == product.jewelry:
				variationNumber = i
				i += 1
			else:
				i += 1
				continue

			# Photos
			j = 1
			for photo in JewelryPhoto.objects.filter(jewelry=variation).order_by("priority"):
				pd = dict()
				pd['path']     = str(photo.photo.url)
				pd['priority'] = photo.priority
				d['photos'].append(pd)
				j += 1

		# Create jewelry group directory
		group = product.jewelry.getGroup()
		groupDirPath = os.path.join(baseDirPath, group)
		if not os.path.isdir(groupDirPath):
			try:
				os.mkdir(groupDirPath)
			except OSError:
				print(f"Creation of the directory '{groupDirPath}' failed.")
				break

		# Create jewelry directory
		group = product.jewelry.getGroup()
		name = product.getTitle() #.replace(" ", "_")
		jewelryDirPath = os.path.join(baseDirPath, group, name)
		if not os.path.isdir(jewelryDirPath):
			try:
				os.mkdir(jewelryDirPath)
			except OSError:
				print(f"Creation of the directory '{jewelryDirPath}' failed.")
				break

		# Create jewelry variation directory
		variationNo = f"Variation_{variationNumber}"
		jewelryVariationDirPath = os.path.join(jewelryDirPath, variationNo)
		if not os.path.isdir(jewelryVariationDirPath):
			try:
				os.mkdir(jewelryVariationDirPath)
			except OSError:
				print(f"Creation of the directory '{jewelryVariationDirPath}' failed.")
				break

		# Write common.txt
		commonFilePath = os.path.join(jewelryDirPath, "common.txt")
		if not os.path.isfile(commonFilePath):
			common_txt = ""
			common_txt += f"brief:       {d['brief']}\n"
			common_txt += f"description: {d['description']}\n"
			common_txt += f"stone:       {d['stone']}\n"
			macrame = bool2YesNo(d['macrame'])
			common_txt += f"macrame:     {macrame}\n"
			common_txt += f"pcolor:      {d['pcolor']}\n"
			common_txt += f"\n"
			common_f = open(commonFilePath, "w")
			common_f.write(common_txt)
			common_f.close()
			#os.sync()
			#print(f"Wrote file to {commonFilePath}")
		#else:
		#	print(f"[ERROR] {commonFilePath} exists!")

		# Copy photos
		for photo in d['photos']:
			no = photo['priority']
			sourcePhotoPath = settings.BASE_DIR + photo['path']
			extension = os.path.splitext(sourcePhotoPath)[1]
			destinationPhotoPath = os.path.join(jewelryVariationDirPath, str(no) + "_" + "photo" + extension)

			try:
				shutil.copyfile(sourcePhotoPath, destinationPhotoPath)
				pass
			except IOError:
				print(f"Failed to copy '{sourcePhotoPath}' to '{destinationPhotoPath}'.")
				break

		# Write info.txt
		infoFilePath = os.path.join(jewelryVariationDirPath, "info.txt")
		info_txt = ""
		info_txt += f"material:          {d['material']}\n"
		info_txt += f"platting:          {d['platting']}\n"
		info_txt += f"scolor:            {d['scolor']}\n"
		info_txt += f"\n"
		info_f = open(infoFilePath, "w")
		info_f.write(info_txt)
		info_f.close()
		#print(f"Wrote file to {infoFilePath}")

		# Write product.txt
		productFilePath = os.path.join(jewelryVariationDirPath, "product.txt")
		product_txt = ""
		product_txt += f"Price:             {d['price']:g}\n"
		isFeatured = bool2YesNo(d['isFeatured'])
		product_txt += f"isFeatured:        {isFeatured}\n"
		isActive = bool2YesNo(d['isActive'])
		product_txt += f"isActive:          {isActive}\n"
		product_txt += f"\n"
		product_f = open(productFilePath, "w")
		product_f.write(product_txt)
		product_f.close()
		#print(f"Wrote file to {productFilePath}")

		# Write common.txt
		groupFilePath = os.path.join(jewelryDirPath, f"{d['group']}.txt")
		if not os.path.isfile(groupFilePath):
			group_txt = ""
			gd = product.getInfo()
			if d['group'] == "Bracelet":
				group_txt += f"diameter_max:   {gd['diameter_max']:g}\n"
				group_txt += f"diameter_min:   {gd['diameter_min']:g}\n"
				group_txt += f"width_max:      {gd['width_max']:g}\n"
				group_txt += f"width_min:      {gd['width_min']:g}\n"
				isAdjustable = bool2YesNo(gd['isAdjustable'])
				group_txt += f"isAdjustable:   {isAdjustable}\n"
			elif d['group'] == "Necklace":
				group_txt += f"length:         {gd['length']:g}\n"
				group_txt += f"width_max:      {gd['width_max']:g}\n"
				group_txt += f"width_min:      {gd['width_min']:g}\n"
				isAdjustable = bool2YesNo(gd['isAdjustable'])
				group_txt += f"isAdjustable:   {isAdjustable}\n"
			elif d['group'] == "Ring":
				group_txt += f"circumference:  {gd['circumference']:g}\n"
				group_txt += f"width_max:      {gd['width_max']:g}\n"
				group_txt += f"width_min:      {gd['width_min']:g}\n"
				isAdjustable = bool2YesNo(gd['isAdjustable'])
				group_txt += f"isAdjustable:   {isAdjustable}\n"
			elif d['group'] == "Earring":
				group_txt += f"heigth:         {gd['heigth']:g}\n"
				group_txt += f"width_max:      {gd['width_max']:g}\n"
				group_txt += f"width_min:      {gd['width_min']:g}\n"

			group_txt += f"\n"
			group_f = open(groupFilePath, "w")
			group_f.write(group_txt)
			group_f.close()
			#print(f"Wrote file to {groupFilePath}")
		#else:
		#	print(f"[ERROR] {groupFilePath} exists!")

		print(f"Exporting: Variant {variationNumber} of {d['group']}    \t{d['title']}")

	os.sync()
	txt = f"Exported {productLen} products to {baseDirPath} successfully."
	print(txt)
