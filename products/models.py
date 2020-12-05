import random
from enum        import Enum
from itertools   import chain

from django.db   import models
from django.urls import reverse
from django.core.files import File
from django.core.exceptions import ValidationError
from django_enum_choices.fields import EnumChoiceField

from .internal.enum import GroupEnum
from .internal.enum import MaterialEnum
from .internal.enum import PlattingEnum
from .internal.enum import FinishEnum
from .internal.enum import StoneEnum
from .internal.enum import ColorEnum


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
			except models.FieldDoesNotExist:
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


class JewelryCommon(AbstractModel):
	title       = models.CharField(max_length=120, unique=True)
	brief       = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	stone       = EnumChoiceField(StoneEnum, default=StoneEnum.N)
	macrame     = models.BooleanField(default=False)
	color       = EnumChoiceField(ColorEnum, default=ColorEnum.N) # Primary Color

	def isRegistered(self):
		theClass = type(self)
		objList = theClass.objects.filter(title=self.title)
		l = len(objList)
		if l == 0:
			return False
		elif l == 1:
			return True
		else:
			raise Exception(f"More that one instance of {self.title} @ {theClass.__name__}")

	def clean(self):
		if self.title == '':
			raise ValidationError('Empty error message')

	@classmethod
	def compare(self, instance):
		pass

	def getStone(self):
		return self.stone.value

	def getMacrame(self):
		return self.macrame

	def getCommonInfo(self):
		info = dict()
		info["stone"]    = self.stone.value
		info["macrame"]  = self.macrame
		return info

	def __str__(self):
		return f"{self.title}"

	class Meta:
		abstract = True


class Bracelet(JewelryCommon):
	diameter_max = models.FloatField() # in cm
	diameter_min = models.FloatField() # in cm
	width_max    = models.FloatField() # in cm
	width_min    = models.FloatField() # in cm
	isAdjustable = models.BooleanField(default=True)

	def getInfo(self):
		#info = dict()
		info = self.getCommonInfo()
		info["diameter_max"] = self.diameter_max
		info["diameter_min"] = self.diameter_min
		info["width_max"]    = self.width_max
		info["width_min"]    = self.width_min
		info["isAdjustable"] = self.isAdjustable
		return info


class Necklace(JewelryCommon):
	length       = models.FloatField() # in cm
	width_max    = models.FloatField() # in cm
	width_min    = models.FloatField() # in cm
	isAdjustable = models.BooleanField(default=True)

	def getInfo(self):
		#info = dict()
		info = self.getCommonInfo()
		info["length"]	     = self.length
		info["width_max"]    = self.width_max
		info["width_min"]    = self.width_min
		info["isAdjustable"] = self.isAdjustable
		return info


class Ring(JewelryCommon):
	circumference = models.FloatField() # in mm
	width_max     = models.FloatField() # in cm
	width_min     = models.FloatField() # in cm
	isAdjustable  = models.BooleanField(default=True)

	def getInfo(self):
		#info = dict()
		info = self.getCommonInfo()
		info["circumference"] = self.circumference
		info["width_max"]     = self.width_max
		info["width_min"]     = self.width_min
		info["isAdjustable"]  = self.isAdjustable
		return info


class Earring(JewelryCommon):
	heigth    = models.FloatField() # in cm
	width_max = models.FloatField() # in cm
	width_min = models.FloatField() # in cm

	def getInfo(self):
		#info = dict()
		info = self.getCommonInfo()
		info["heigth"]    = self.heigth
		info["width_max"] = self.width_max
		info["width_min"] = self.width_min
		return info


class JewelryGroup(AbstractModel):
	# RnD new function for 1 to 1
	group    = EnumChoiceField(GroupEnum, default=GroupEnum.N)
	bracelet = models.ForeignKey(Bracelet, blank=True, null=True, on_delete=models.CASCADE)
	necklace = models.ForeignKey(Necklace, blank=True, null=True, on_delete=models.CASCADE)
	ring     = models.ForeignKey(Ring,     blank=True, null=True, on_delete=models.CASCADE)
	earring  = models.ForeignKey(Earring,  blank=True, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.getTitle()} | {self.group.value}"

	def getInfo(self):
		if self.group == GroupEnum.N:
			info = None
		elif self.group == GroupEnum.BR:
			info = self.bracelet.getInfo()
		elif self.group == GroupEnum.NE:
			info = self.necklace.getInfo()
		elif self.group == GroupEnum.RI:
			info = self.ring.getInfo()
		elif self.group == GroupEnum.EA:
			info = self.earring.getInfo()
		return info

	def getTitle(self):
		title = None
		if self.group == GroupEnum.N:
			title = "ERROR"
		elif self.group == GroupEnum.BR:
			title = f"{self.bracelet}"
		elif self.group == GroupEnum.NE:
			title = f"{self.necklace}"
		elif self.group == GroupEnum.RI:
			title = f"{self.ring}"
		elif self.group == GroupEnum.EA:
			title = f"{self.earring}"
		return title

	def getBrief(self):
		brief = None
		if self.group == GroupEnum.N:
			brief = "ERROR"
		elif self.group == GroupEnum.BR:
			brief = f"{self.bracelet.brief}"
		elif self.group == GroupEnum.NE:
			brief = f"{self.necklace.brief}"
		elif self.group == GroupEnum.RI:
			brief = f"{self.ring.brief}"
		elif self.group == GroupEnum.EA:
			brief = f"{self.earring.brief}"
		return brief


	def getDescription(self):
		description = None
		if self.group == GroupEnum.N:
			description = "ERROR"
		elif self.group == GroupEnum.BR:
			description = f"{self.bracelet.description}"
		elif self.group == GroupEnum.NE:
			description = f"{self.necklace.description}"
		elif self.group == GroupEnum.RI:
			description = f"{self.ring.description}"
		elif self.group == GroupEnum.EA:
			description = f"{self.earring.description}"
		return description


	def getStone(self):
		if self.group == GroupEnum.N:
			stone = "ERROR"
		elif self.group == GroupEnum.BR:
			stone = f"{self.bracelet.getStone()}"
		elif self.group == GroupEnum.NE:
			stone = f"{self.necklace.getStone()}"
		elif self.group == GroupEnum.RI:
			stone = f"{self.ring.getStone()}"
		elif self.group == GroupEnum.EA:
			stone = f"{self.earring.getStone()}"
		return stone


	def getMacrame(self):
		if self.group == GroupEnum.N:
			macrame = "ERROR"
		elif self.group == GroupEnum.BR:
			macrame = f"{self.bracelet.getMacrame()}"
		elif self.group == GroupEnum.NE:
			macrame = f"{self.necklace.getMacrame()}"
		elif self.group == GroupEnum.RI:
			macrame = f"{self.ring.getMacrame()}"
		elif self.group == GroupEnum.EA:
			macrame = f"{self.earring.getMacrame()}"
		return macrame


	def getPrimaryColor(self):
		color = None
		if self.group == GroupEnum.N:
			color = "ERROR"
		elif self.group == GroupEnum.BR:
			color = f"{self.bracelet.color.value}"
		elif self.group == GroupEnum.NE:
			color = f"{self.necklace.color.value}"
		elif self.group == GroupEnum.RI:
			color = f"{self.ring.color.value}"
		elif self.group == GroupEnum.EA:
			color = f"{self.earring.color.value}"
		return color

	class Meta:
		db_table = 'JewelryGroup'


class Jewelry(AbstractModel):
	group    = models.ForeignKey(JewelryGroup, on_delete=models.CASCADE)
	material = EnumChoiceField(MaterialEnum, default=MaterialEnum.N)
	platting = EnumChoiceField(PlattingEnum, default=PlattingEnum.N)

	def getGroup(self):
		return self.group.group.value

	def getMaterial(self):
		return self.material.value

	def getPlatting(self):
		return self.platting.value

	def getInfo(self):
		info = dict()
		info["type"]     = "Jewelry"
		info["group"]    = self.group.group.value
		info["material"] = self.material.value
		info["platting"] = self.platting.value
		return {**info, **self.group.getInfo()}

	def __str__(self):
		return f"{self.group} | {self.material.value} | {self.platting.value}"

	def get_absolute_url(self):
		return reverse("products:product-detail", kwargs={"id": self.id})

	def getTitle(self):
		return f"{self.group.getTitle()}"
	getTitle.short_description = 'Title'

	def getBrief(self):
		return f"{self.group.getBrief()}"

	def getDescription(self):
		return f"{self.group.getDescription()}"

	def getStone(self):
		return f"{self.group.getStone()}"

	def getMacrame(self):
		return f"{self.group.getMacrame()}"

	def getPhotos(self):
		photos = JewelryPhoto.objects.filter(jewelry=self).order_by("priority") #.first()
		l = len(photos)
		#for p in photos:
		#    pass
		return f"{l} |          {photos}"

	def getRandomObject(self):
		objList = Jewelry.objects.all()
		obj = random.choice(objList)
		return obj

	def getPrimaryColor(self):
		return self.group.getPrimaryColor()

	class Meta:
		db_table = 'Jewelry'
		#order_with_respect_to = 'material'


class JewelryPhoto(AbstractModel):
	photo    = models.ImageField(upload_to='img/jewelryPhoto', blank=False)
	jewelry  = models.ForeignKey(Jewelry, on_delete=models.CASCADE)
	priority = models.DecimalField(decimal_places=0, max_digits=2)

	def __str__(self):
		return f"{self.jewelry} | {self.photo}"

	class Meta:
		db_table = 'JewelryPhoto'


class JewelryColor(AbstractModel):
	color   = EnumChoiceField(ColorEnum, default=ColorEnum.N) # Secondary color
	jewelry = models.ForeignKey(Jewelry, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.jewelry} | {self.color.value}"

	def getPhotoUrl(self):
		obj = JewelryPhoto.objects.filter(jewelry = self.jewelry).order_by("priority").first()
		try:
			txt = obj.photo.url
		except IndexError:
			txt = "/static/img/jewelry-placeholder.jpg"
		except AttributeError:
			txt = "/static/img/jewelry-placeholder.jpg"
		return f"{txt}"

	class Meta:
		db_table = 'JewelryColor'


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

	def getNextObject(self):
		obj = Product.objects.get_next_by_number(Product, id=self.id)
		return self

	def getInfo(self):
		return self.jewelry.getInfo()

	class Meta:
		db_table = 'Product'


class ProductTool():

	def create(dictionary):
		className = __class__.__name__
		if not isinstance(dictionary, dict):
			raise Exception(f"Needs a dictionary to create {className}")

		#print(dictionary)

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
