from django.db import models
from django.urls import reverse

from django.core.files import File
from .internal.models import Jewelry
from .internal.models import Bracelet
from .internal.models import Ring
from .internal.models import Necklace
from .internal.models import Earring
from .internal.models import JewelryGroup
from .internal.models import JewelryPhoto

from .internal.utils import AbstractModel
from .internal.utils import random_price
from .internal.utils import random_bool
from .internal.utils import random_line
from .internal.utils import getRandomPhotoList

from .internal.enum import GroupEnum
from .internal.enum import MaterialEnum
from .internal.enum import PlattingEnum
from .internal.enum import StoneEnum
from .internal.enum import ColorEnum

import hashlib
import random


class JewelryProductManager(models.Manager):

	def get_queryset(self):
		return super().get_queryset()

	def active(self):
		return self.get_queryset().filter(isActive=True).order_by('sku')

	def featured(self):
		return self.active().filter(isFeatured=True)[:10]

	def rings(self):
		JewelryGroupList = JewelryGroup.objects.filter(group=GroupEnum.RI)
		return self.active().filter(jewelry__group__in=JewelryGroupList)

	def bracelets(self):
		JewelryGroupList = JewelryGroup.objects.filter(group=GroupEnum.BR)
		return self.active().filter(jewelry__group__in=JewelryGroupList)

	def necklaces(self):
		JewelryGroupList = JewelryGroup.objects.filter(group=GroupEnum.NE)
		return self.active().filter(jewelry__group__in=JewelryGroupList)

	def earrings(self):
		JewelryGroupList = JewelryGroup.objects.filter(group=GroupEnum.EA)
		return self.active().filter(jewelry__group__in=JewelryGroupList)

	def macrame(self):
		RingList = Ring.objects.filter(macrame=False)
		BraceletList = Bracelet.objects.filter(macrame=False)
		NecklaceList = Necklace.objects.filter(macrame=False)
		EarringList = Earring.objects.filter(macrame=False)

		JewelryGroupList = JewelryGroup.objects.all()
		JewelryGroupList = JewelryGroupList.exclude(ring__in=RingList)
		JewelryGroupList = JewelryGroupList.exclude(bracelet__in=BraceletList)
		JewelryGroupList = JewelryGroupList.exclude(necklace__in=NecklaceList)
		JewelryGroupList = JewelryGroupList.exclude(earring__in=EarringList)

		return self.active().filter(jewelry__group__in=JewelryGroupList)

	def silver925(self):
		return self.active().filter(jewelry__material=MaterialEnum.SI)

	def brass(self):
		return self.active().filter(jewelry__material=MaterialEnum.BR)

	def metal(self):
		return self.active().exclude(jewelry__material=MaterialEnum.N)


class Product(AbstractModel):

	def get_sku(self):

		title = self.jewelry.getTitle()

		group = str(self.jewelry.getGroup())[0:1].upper()
		hashedTitle = hashlib.md5(title.encode()).hexdigest()[:10].upper()
		stoneId = self.jewelry.getStone().getId()
		pColorId = str(self.jewelry.getPrimaryColor().getId())
		macrame = str(self.jewelry.getMacrame()[0]).upper()

		material = str(self.jewelry.getMaterial().getId())
		platting = str(self.jewelry.platting.value)[0].upper()
		sColorId = str(self.jewelry.getSecondaryColor().getId())

		rv = f"0-LJ-J-{group}-{hashedTitle}-S{stoneId}C{pColorId}{sColorId}-{macrame}{material}{platting}"
		return rv

	sku = models.TextField(default=None, blank=False, null=False, editable=False)
	price = models.FloatField(blank=False, null=False)
	isFeatured = models.BooleanField(default=False)
	isActive = models.BooleanField(default=True)
	jewelry = models.OneToOneField(Jewelry, on_delete=models.CASCADE, primary_key=False)

	objects = JewelryProductManager()

	def save(self, *args, **kwargs):

		self.sku = self.get_sku()

		super().save(*args, **kwargs)

	def __str__(self):
		return str(self.jewelry)

	def get_absolute_url(self):
		return reverse("products:detail", kwargs={"id": self.id})

	def get_absolute_addTocart_url(self):
		return reverse("cart:add", kwargs={"product_id": self.id})

	def getTitle(self):
		return str(self.jewelry.getTitle())
	getTitle.short_description = 'Title'

	def getPrice(self):
		return str(self.price)

	def getBrief(self):
		return self.jewelry.getBrief()

	def getDescription(self):
		return self.jewelry.getDescription()

	def getPhoto(self):
		obj = JewelryPhoto.objects.filter(jewelry=self.jewelry).order_by("priority").first()
		return obj

	def getPhotoList(self):
		obj = JewelryPhoto.objects.filter(jewelry=self.jewelry).order_by("priority")
		return obj

	def getColorList(self):
		colorList = list()
		number = 1

		primaryColor = self.jewelry.getPrimaryColor()
		if primaryColor != ColorEnum.N:
			d = {"no": number, "color": primaryColor.value}
			colorList.append(d)
			number += 1

		secondaryColor = self.jewelry.getSecondaryColor()
		if secondaryColor != ColorEnum.N:
			d = {"no": number, "color": secondaryColor.value}
			colorList.append(d)
			number += 1

		return colorList

	def getPrevObject(self):
		obj = Product.objects.filter(id__lt=self.id).order_by('id').last()
		return obj

	def getNextObject(self):
		obj = Product.objects.filter(id__gt=self.id).order_by('id').first()
		return obj

	def getInfo(self):
		return self.jewelry.getInfo()

	def _create_random():
		# Make sure group is not None
		group = GroupEnum.N
		while group == GroupEnum.N:
			group = GroupEnum.random()

		dictionary = dict()

		# Product
		# dictionary["sku"]          = "?"
		dictionary["price"] = random_price()
		dictionary["isFeatured"] = random_bool()
		dictionary["isActive"] = random_bool()

		# Jewelry Common
		dictionary["title"] = random_line('tests/products/titleList')
		dictionary["brief"] = random_line('tests/products/briefList')
		dictionary["description"] = "Default description..."
		dictionary["stone"] = StoneEnum.random()
		dictionary["macrame"] = random_bool()
		dictionary["pcolor"] = ColorEnum.random()

		# Jewelry Variation
		dictionary["material"] = MaterialEnum.random()
		dictionary["platting"] = PlattingEnum.random()
		dictionary["group"] = group

		dictionary["heigth"] = int(random.uniform(0, 999))
		dictionary["length"] = int(random.uniform(0, 999))
		dictionary["circumference"] = int(random.uniform(0, 999))
		dictionary["width_max"] = int(random.uniform(0, 999))
		dictionary["width_min"] = int(random.uniform(0, 999))
		dictionary["diameter_max"] = int(random.uniform(0, 999))
		dictionary["diameter_min"] = int(random.uniform(0, 999))
		dictionary["isAdjustable"] = random_bool()

		dictionary["photos"] = getRandomPhotoList("pages/static/delete/jewel3/")
		dictionary["scolor"] = ColorEnum.random()

		# Invalid
		dictionary["invalid"] = "Invalid dictionary keys are ignored!"

		return ProductTool.create(dictionary)

	class Meta:
		db_table = 'Product'


class ProductTool():

	def createFromForm(d):

		def getDictValue(d, key, default=None):
			try:
				v = d[key]
			except Exception:
				v = default

			return v

		dictionary = dict()

		# Product
		dictionary["price"] = d["price"]
		dictionary["isFeatured"] = d["isFeatured"]
		dictionary["isActive"] = d["isActive"]

		# Jewelry Common
		dictionary["title"] = d['title']
		dictionary["brief"] = d['brief']
		dictionary["description"] = d['description']
		dictionary["stone"] = StoneEnum.str2Enum(d['stone'])
		dictionary["macrame"] = d['macrame']
		dictionary["pcolor"] = ColorEnum.str2Enum(d['pcolor'])

		# Jewelry Variation
		dictionary["material"] = MaterialEnum.str2Enum(d['material'])
		dictionary["platting"] = PlattingEnum.str2Enum(d['platting'])
		dictionary["group"] = GroupEnum.str2Enum(d['group'])

		dictionary["heigth"] = getDictValue(d, 'heigth')
		dictionary["length"] = getDictValue(d, 'length')
		dictionary["circumference"] = getDictValue(d, 'circumference')
		dictionary["width_max"] = getDictValue(d, 'width_max')
		dictionary["width_min"] = getDictValue(d, 'width_min')
		dictionary["diameter_max"] = getDictValue(d, 'diameter_max')
		dictionary["diameter_min"] = getDictValue(d, 'diameter_min')
		dictionary["isAdjustable"] = getDictValue(d, 'isAdjustable')

		dictionary["photos"] = d["photos"]
		dictionary["scolor"] = ColorEnum.str2Enum(d['scolor'])

		return ProductTool.create(dictionary)

	def create(dictionary):
		className = __class__.__name__

		def vprint(s):
			# print(s)
			pass

		# Check arguments
		if not isinstance(dictionary, dict):
			raise Exception(f"Needs a dictionary to create {className}")

		# Get group so as to decide
		def getGroupClass(group):
			if group == GroupEnum.N:
				# raise Exception("Group is None")
				print("Group is None")
				exit()
			elif group == GroupEnum.BR:
				c = Bracelet
			elif group == GroupEnum.NE:
				c = Necklace
			elif group == GroupEnum.RI:
				c = Ring
			elif group == GroupEnum.EA:
				c = Earring
			else:
				raise Exception(f"{group} is not a registered jewelry group")
			return c

		################################################################
		# Create the jewelry
		groupClass = getGroupClass(dictionary["group"])
		baseJewelryObj = groupClass.create(dictionary)
		# print(baseJewelryObj.to_txt())
		isBaseJewelryRegistered = baseJewelryObj.isRegistered()
		# Ring.isRegistered()

		# Check if name already exists
		if isBaseJewelryRegistered is True:
			print(f"{baseJewelryObj} @ {groupClass.__name__} is already available!")
			baseJewelryObj = groupClass.objects.filter(title=dictionary["title"]).first()
		else:
			try:
				baseJewelryObj.save()
			except AttributeError:
				raise Exception(f"Failed to save JewelryGroup '{baseJewelryObj}'")

			vprint(f"Created {baseJewelryObj}")

		vprint(baseJewelryObj.to_txt())

		################################################################
		# Create the jewelryGroup
		def buildJewelryGroup(group, jewelryObj):
			bracelet = None
			earring = None
			necklace = None
			ring = None

			if group == GroupEnum.N:
				# raise Exception("Group is None")
				print("Group is None")
				exit()
			elif group == GroupEnum.BR:
				bracelet = jewelryObj
			elif group == GroupEnum.NE:
				necklace = jewelryObj
			elif group == GroupEnum.RI:
				ring = jewelryObj
			elif group == GroupEnum.EA:
				earring = jewelryObj
			else:
				raise Exception(f"{group} is not a registered jewelry group")
			return JewelryGroup(group=group, bracelet=bracelet, earring=earring, necklace=necklace, ring=ring)

		if isBaseJewelryRegistered is True:
			# So jewelryGroup is SHOULD  also be available
			def locateJewelryGroup(group, jewelryObj):
				if group == GroupEnum.N:
					# raise Exception("Group is None")
					print("Group is None")
					exit()
				elif group == GroupEnum.BR:
					obj = JewelryGroup.objects.filter(bracelet=jewelryObj)
				elif group == GroupEnum.NE:
					obj = JewelryGroup.objects.filter(necklace=jewelryObj)
				elif group == GroupEnum.RI:
					obj = JewelryGroup.objects.filter(ring=jewelryObj)
				elif group == GroupEnum.EA:
					obj = JewelryGroup.objects.filter(earring=jewelryObj)
				else:
					raise Exception(f"{group} is not a registered jewelry group")
				objLen = len(obj)
				obj = obj.first()
				if objLen == 0:
					raise Exception(f"Could not find the JewelryGroup for {jewelryObj}")
				elif objLen != 1:
					raise Exception(f"Found more that one JewelryGroup for {jewelryObj}")
				return obj

			jewelryGroupObj = locateJewelryGroup(dictionary["group"], baseJewelryObj)
			print(f"{jewelryGroupObj} is already available!")
		else:
			try:
				jewelryGroupObj = buildJewelryGroup(dictionary["group"], baseJewelryObj)
			except AttributeError:
				raise Exception(f"Failed to create '{jewelryGroupObj}'")
			try:
				jewelryGroupObj.save()
			except AttributeError:
				raise Exception(f"Failed to save JewelryGroup '{jewelryGroupObj}'")

			vprint(f"Created {jewelryGroupObj}")

		vprint(jewelryGroupObj.to_txt())

		################################################################
		# Create the jewelryVariation

		jewelryVariationObj = Jewelry(
			group=jewelryGroupObj,
			material=dictionary["material"],
			platting=dictionary["platting"],
			scolor=dictionary["scolor"]
		)

		# Check if name already exists
		try:
			jewelryVariationObj.save()
		except AttributeError:
			raise Exception(f"Failed to save JewelryVariation: '{jewelryVariationObj}'")

		vprint(f"Created {jewelryVariationObj}")
		vprint(jewelryVariationObj.to_txt())

		################################################################
		# Create the jewelryPhotos

		i = 1
		sortedPhotoList = dictionary["photos"]
		sortedPhotoList.sort()
		for photo in sortedPhotoList:
			jewelryPhotoObj = JewelryPhoto(
				photo=photo,
				jewelry=jewelryVariationObj,
				priority=i
			)
			i += 1

			try:
				jewelryPhotoObj.photo.save(f'{dictionary["title"]}.jpg', File(open(photo, 'rb')), save=True)
				# jewelryPhotoObj.save()
			except Exception:
				raise Exception(f"Could not save {photo}")

			vprint(f"Created {jewelryPhotoObj}")
			vprint(jewelryPhotoObj.to_txt())

		################################################################
		# Create the product

		productObj = Product(
			price=dictionary["price"],
			isFeatured=dictionary["isFeatured"],
			isActive=dictionary["isActive"],
			jewelry=jewelryVariationObj
		)

		# Check if name already exists
		try:
			productObj.save()
		except AttributeError:
			raise Exception(f"Failed to save Product '{productObj}'")

		print(f"Created {productObj}")
		print(productObj.to_txt())

		return productObj
