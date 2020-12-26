#from enum        import Enum

from django.core.exceptions import ValidationError
from django.db              import models
from django.urls            import reverse

from django_enum_choices.fields import EnumChoiceField

from .enum  import GroupEnum
from .enum  import MaterialEnum
from .enum  import PlattingEnum
from .enum  import FinishEnum
from .enum  import StoneEnum
from .enum  import ColorEnum

from .utils  import AbstractModel

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
			txt = "/static/img/shop/placeholder.jpg"
		except AttributeError:
			txt = "/static/img/shop/placeholder.jpg"
		return f"{txt}"

	class Meta:
		db_table = 'JewelryColor'
