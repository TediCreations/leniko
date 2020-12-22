from django.db   import models
from django.urls import reverse
from django.core.files import File
from django.core.exceptions import ValidationError
from django_enum_choices.fields import EnumChoiceField

from .internal.models import Jewelry
from .internal.models import Bracelet
from .internal.models import Ring
from .internal.models import Necklace
from .internal.models import Earring
from .internal.models import JewelryGroup
from .internal.models import JewelryPhoto
from .internal.models import JewelryColor

from .internal.utils  import AbstractModel

from .internal.enum   import GroupEnum
from .internal.enum   import MaterialEnum
from .internal.enum   import PlattingEnum
from .internal.enum   import FinishEnum
from .internal.enum   import StoneEnum
from .internal.enum   import ColorEnum



class Product(AbstractModel):
	#sku       = https://getshogun.com/learn/sku-generator | https://en.wikipedia.org/wiki/Stock_keeping_unit
	sku        = models.TextField(blank=False, null=False)
	price      = models.FloatField()
	isFeatured = models.BooleanField(default=False)
	isActive   = models.BooleanField(default=True)
	jewelry    = models.OneToOneField(Jewelry, on_delete=models.CASCADE, primary_key=False)

	def __str__(self):
		return str(self.jewelry)

	def get_absolute_url(self):
		return reverse("products:product-detail", kwargs={"id": self.id})

	def getTitle(self):
		return str(self.jewelry.getTitle())
	getTitle.short_description = 'Title'

	def getPrice(self):
		return str(self.price)

	def getBrief(self):
		return self.jewelry.getBrief()

	def getDescription(self):
		return self.jewelry.getDescription()

	def getPhotoUrl(self):
		obj = JewelryPhoto.objects.filter(jewelry = self.jewelry).order_by("priority").first()
		try:
			txt = obj.photo.url
		except IndexError:
			txt = "/static/img/jewelry-placeholder.jpg"
		except AttributeError:
			txt = "/static/img/jewelry-placeholder.jpg"
		return f"{txt}"

	def getPhoto(self):
		obj = JewelryPhoto.objects.filter(jewelry = self.jewelry).order_by("priority").first()
		try:
			p = obj.photo
		except IndexError:
			p = None
		except AttributeError:
			p = None
		return p


	def getPhotoList(self):
		obj = JewelryPhoto.objects.filter(jewelry = self.jewelry).order_by("priority")
		l = list()
		number = 1
		for o in obj:
			d = { "no": number, "url": o.photo.url, "priority": o.priority}
			l.append(d)
			number += 1
		if len(l) is 0:
			d = { "no": 1, "url": "/static/img/jewelry-placeholder.jpg", "priority": 0}
			l.append(d)
		return l


	def getColorList(self):
		obj = JewelryColor.objects.filter(jewelry = self.jewelry).order_by("color")
		l = list()
		number = 1
		primaryColor = self.jewelry.getPrimaryColor()
		if primaryColor is not "None":
			d = { "no": number, "color": primaryColor}
			l.append(d)
			number += 1
		for o in obj:
			secondaryColor = o.color.value
			if secondaryColor is not "None" and secondaryColor is not primaryColor:
				d = { "no": number, "color": secondaryColor}
				l.append(d)
				number += 1
		return l

	def getNoOfPhotos(self):
		obj = JewelryPhoto.objects.filter(jewelry = self.jewelry)
		return len(obj)

	def getPrevObject(self):
		obj = Product.objects.filter(id__lt=self.id).order_by('id').last()
		return obj

	def getNextObject(self):
		obj = Product.objects.filter(id__gt=self.id).order_by('id').first()
		return obj

	def getInfo(self):
		return self.jewelry.getInfo()

	class Meta:
		db_table = 'Product'


class ProductTool():

	def create(dictionary):
		className = __class__.__name__

		# Check arguments
		if not isinstance(dictionary, dict):
			raise Exception(f"Needs a dictionary to create {className}")

		# Get group so as to decide
		def getGroupClass(group):
			if group == GroupEnum.N:
				#raise Exception("Group is None")
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
		#print(baseJewelryObj.to_txt())
		isBaseJewelryRegistered = baseJewelryObj.isRegistered()
		#Ring.isRegistered()

		# Check if name already exists
		if isBaseJewelryRegistered is True:
			print(f"{baseJewelryObj} @ {groupClass.__name__} is already available!")
			baseJewelryObj = groupClass.objects.filter(title=dictionary["title"]).first()
		else:
			try:
				baseJewelryObj.save()
			except AttributeError as e:
				raise Exception(f"Failed to save '{baseJewelryObj}'")

			print(f"Created {baseJewelryObj}")

		print(baseJewelryObj.to_txt())

		################################################################
		# Create the jewelryGroup
		def buildJewelryGroup(group, jewelryObj):
			bracelet = None
			earring  = None
			necklace = None
			ring     = None
			if group == GroupEnum.N:
				#raise Exception("Group is None")
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
					#raise Exception("Group is None")
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
				l = len(obj)
				obj = obj.first()
				if l == 0:
					raise Exception(f"Could not find the JewelryGroup for {jewelryObj}")
				elif l != 1:
					raise Exception(f"Found more that one JewelryGroup for {jewelryObj}")
				return obj

			jewelryGroupObj = locateJewelryGroup(dictionary["group"], baseJewelryObj)
			print(f"{jewelryGroupObj} is already available!")
		else:
			try:
				jewelryGroupObj = buildJewelryGroup(dictionary["group"], baseJewelryObj)
			except AttributeError as e:
				raise Exception(f"Failed to create '{jewelryGroupObj}'")
			try:
				jewelryGroupObj.save()
			except AttributeError as e:
				raise Exception(f"Failed to save '{jewelryGroupObj}'")

			print(f"Created {jewelryGroupObj}")

		print(jewelryGroupObj.to_txt())

		################################################################
		# Create the jewelryVariation

		jewelryVariationObj = Jewelry(group    = jewelryGroupObj,
					      material = dictionary["material"],
					      platting = dictionary["platting"])

		# Check if name already exists
		try:
			jewelryVariationObj.save()
		except AttributeError as e:
			raise Exception(f"Failed to save '{jewelryVariationObj}'")

		print(f"Created {jewelryVariationObj}")
		print(jewelryVariationObj.to_txt())

		################################################################
		# Create the jewelryPhotos

		i = 1
		sortedPhotoList = dictionary["photos"]
		sortedPhotoList.sort()
		for photo in sortedPhotoList:
			jewelryPhotoObj = JewelryPhoto(
				photo    = photo,
				jewelry  = jewelryVariationObj,
				priority = i
			)
			i += 1

			try:
				jewelryPhotoObj.photo.save(f'{dictionary["group"].value}_{dictionary["title"]}.jpg', File(open(photo, 'rb')), save=True)
				#jewelryPhotoObj.save()
			except Exception:
				raise Exception("Could not save {photo}")

			print(f"Created {jewelryPhotoObj}")
			print(jewelryPhotoObj.to_txt())

		################################################################
		# Create the jewelryColors

		for color in dictionary["colors"]:
			jewelryColorObj = JewelryColor(
				jewelry  = jewelryVariationObj,
				color    = color
			)
			jewelryColorObj.save()

			print(f"Created {jewelryColorObj}")
			print(jewelryColorObj.to_txt())

		################################################################
		# Create the product

		import uuid
		productObj = Product(sku        = str(uuid.uuid4()),
				     price      = dictionary["price"],
				     isFeatured = dictionary["isFeatured"],
				     isActive   = dictionary["isActive"],
				     jewelry    = jewelryVariationObj
		)

		# Check if name already exists
		try:
			productObj.save()
		except AttributeError as e:
			raise Exception(f"Failed to save '{productObj}'")

		print(f"Created {productObj}")
		print(productObj.to_txt())
