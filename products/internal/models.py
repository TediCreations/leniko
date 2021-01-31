from django.core.exceptions import ValidationError
from django.db              import models
from django.urls            import reverse

from django_enum_choices.fields import EnumChoiceField
from sorl.thumbnail             import ImageField
from sorl.thumbnail             import get_thumbnail
from sorl.thumbnail             import delete


from .enum  import GroupEnum
from .enum  import MaterialEnum
from .enum  import PlattingEnum
from .enum  import FinishEnum
from .enum  import StoneEnum
from .enum  import ColorEnum

from .utils  import AbstractModel

from enum import Enum


class JewelryCommon(AbstractModel):
	title       = models.CharField(max_length=120, unique=True)
	brief       = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	stone       = EnumChoiceField(StoneEnum, default=StoneEnum.N)
	macrame     = models.BooleanField(default=False)
	pcolor      = EnumChoiceField(ColorEnum, default=ColorEnum.N) # Primary Color

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

	#@classmethod
	#def compare(self, instance):
	#	pass

	def getStone(self):
		return self.stone

	def getMacrame(self):
		return self.macrame

	def getCommonInfo(self):
		info = dict()
		info["stone"]    = self.stone.getName()
		info["macrame"]  = self.macrame
		return info

	def __str__(self):
		return f"{self.title}"

	class Meta:
		abstract = True


class Bracelet(JewelryCommon):
	diameter_max = models.FloatField(blank=True, null=True) # in cm
	diameter_min = models.FloatField(blank=True, null=True) # in cm
	width_max    = models.FloatField(blank=True, null=True) # in cm
	width_min    = models.FloatField(blank=True, null=True) # in cm
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
	length       = models.FloatField(blank=True, null=True) # in cm
	width_max    = models.FloatField(blank=True, null=True) # in cm
	width_min    = models.FloatField(blank=True, null=True) # in cm
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
	circumference = models.FloatField(blank=True, null=True) # in mm
	width_max     = models.FloatField(blank=True, null=True) # in cm
	width_min     = models.FloatField(blank=True, null=True) # in cm
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
	heigth    = models.FloatField(blank=True, null=True) # in cm
	width_max = models.FloatField(blank=True, null=True) # in cm
	width_min = models.FloatField(blank=True, null=True) # in cm

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
			description = None
		elif self.group == GroupEnum.BR:
			description = self.bracelet.description
		elif self.group == GroupEnum.NE:
			description = self.necklace.description
		elif self.group == GroupEnum.RI:
			description = self.ring.description
		elif self.group == GroupEnum.EA:
			description = self.earring.description

		return description


	def getStone(self):
		if self.group == GroupEnum.N:
			stone = "ERROR"
		elif self.group == GroupEnum.BR:
			stone = self.bracelet.getStone()
		elif self.group == GroupEnum.NE:
			stone = self.necklace.getStone()
		elif self.group == GroupEnum.RI:
			stone = self.ring.getStone()
		elif self.group == GroupEnum.EA:
			stone = self.earring.getStone()
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
		pcolor = None
		if self.group == GroupEnum.N:
			pcolor = None
		elif self.group == GroupEnum.BR:
			pcolor = self.bracelet.pcolor
		elif self.group == GroupEnum.NE:
			pcolor = self.necklace.pcolor
		elif self.group == GroupEnum.RI:
			pcolor = self.ring.pcolor
		elif self.group == GroupEnum.EA:
			pcolor = self.earring.pcolor
		return pcolor


	class Meta:
		db_table = 'JewelryGroup'


class Jewelry(AbstractModel):
	group    = models.ForeignKey(JewelryGroup, on_delete=models.CASCADE)
	material = EnumChoiceField(MaterialEnum, default=MaterialEnum.N)
	platting = EnumChoiceField(PlattingEnum, default=PlattingEnum.N)
	scolor   = EnumChoiceField(ColorEnum, default=ColorEnum.N) # Secondary Color


	def getGroup(self):
		return self.group.group.value


	def getMaterial(self):
		return self.material


	def getPlatting(self):
		return self.platting.value


	def getInfo(self):
		info = dict()
		info["type"]     = "Jewelry"
		info["group"]    = self.group.group.value
		info["material"] = self.material.getName()
		info["platting"] = self.platting.value
		return {**info, **self.group.getInfo()}


	def __str__(self):
		return f"{self.group} | {self.material.getName()} | {self.platting.value}"


	def get_absolute_url(self):
		return reverse("products:product-detail", kwargs={"id": self.id})


	def getTitle(self):
		return f"{self.group.getTitle()}"
	getTitle.short_description = 'Title'


	def getBrief(self):
		return f"{self.group.getBrief()}"


	def getDescription(self):
		return self.group.getDescription()


	def getStone(self):
		return self.group.getStone()


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


	def getSecondaryColor(self):
		return self.scolor


	class Meta:
		db_table = 'Jewelry'
		#order_with_respect_to = 'material'


class JewelryPhoto(AbstractModel):

	def uploadTo(self, filename):

		groupName = self.jewelry.getGroup().lower()
		#priority  = self.priority
		title     = self.jewelry.getTitle()
		title = title.replace(" ", "__")
		title = title.replace("&", "_and_")

		filename = filename.replace(" ", "__")
		filename = filename.replace("&", "_and_")

		filepath = f'img/jewelry/{groupName}/{title}/{filename}'
		return filepath


	photo   = models.ImageField(upload_to=uploadTo, blank=False)
	jewelry  = models.ForeignKey(Jewelry, on_delete=models.CASCADE)
	priority = models.DecimalField(decimal_places=0, max_digits=2)

	class ThumbnailModeEnum(Enum):
		admin     = "35x35"
		thumbnail = "120x150"
		product   = "328x437"
		big       = "570x760"
		gallery   = "810x1080"

		def getGeometry(self):
			return self.value

		def getName(self):
			return str(self.name)


	def __str__(self):
		return f"{self.jewelry} | {self.photo}"


	def getPhoto(self, mode=None):
		"""Get thumbnail or generate it"""

		# We do not want thumbnails
		if mode == None:
			return self.photo

		# Get mode
		geometry = None

		isValid = False
		for e in self.ThumbnailModeEnum:
			if e.getName() == mode:
				geometry = e.getGeometry()
				isValid = True
				break

		if not isValid:
			return self.photo

		if geometry != None:
			#{% thumbnail photo "?x?" crop="center" padding=True quality=80 upscale=True as im2 %}
			return get_thumbnail(self.photo, geometry_string=geometry, colorspace='RGB', crop='center', padding=True, quality=80)
		else:
			return self.photo


	def save(self, *args, **kwargs):

		# On edit
		# Delete old thumbnails
		# Is the old photo the same as the new?
		delete(self.photo, delete_file=False)

		# Create new
		for e in self.ThumbnailModeEnum:
			self.getPhoto(e.getName())

		super().save(*args, **kwargs)


	def delete(self, *args, **kwargs):
		# Delete thumbnails and original image
		delete(self.photo)

		super().delete(*args, **kwargs)


	class Meta:
		db_table = 'JewelryPhoto'
