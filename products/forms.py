from django import forms

from .internal.enum import GroupEnum
from .internal.enum import StoneEnum
from .internal.enum import ColorEnum
from .internal.enum import MaterialEnum
from .internal.enum import PlattingEnum


class ProductForm(forms.Form):
	price = forms.FloatField()
	isFeatured = forms.BooleanField(required=False, initial=False)
	isActive = forms.BooleanField(required=False, initial=True)


class JewelryCommonForm(ProductForm):
	title = forms.CharField(max_length=120, min_length=1)
	brief = forms.CharField(required=False)
	description = forms.CharField(required=False)
	stone = forms.ChoiceField(choices=StoneEnum.choices(), initial=StoneEnum.N)
	pcolor = forms.ChoiceField(choices=ColorEnum.choices(), initial=ColorEnum.N)
	macrame = forms.BooleanField(required=False, initial=False)

	material = forms.ChoiceField(choices=MaterialEnum.choices(), initial=MaterialEnum.N)
	platting = forms.ChoiceField(choices=PlattingEnum.choices(), initial=PlattingEnum.N)

	photos = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
	# scolor = forms.MultipleChoiceField(required=False, choices = ColorEnum.choices(), widget=forms.SelectMultiple(), initial=ColorEnum.N)
	scolor = forms.ChoiceField(choices=ColorEnum.choices(), initial=ColorEnum.N)


class BraceletForm(JewelryCommonForm):
	group = forms.ChoiceField(widget=forms.HiddenInput(), choices=GroupEnum.choices(), initial=GroupEnum.BR.value)
	diameter_max = forms.FloatField(required=False, initial=None)  # in cm
	diameter_min = forms.FloatField(required=False, initial=None)  # in cm
	width_max = forms.FloatField(required=False, initial=None)  # in cm
	width_min = forms.FloatField(required=False, initial=None)  # in cm
	isAdjustable = forms.BooleanField(required=False, initial=True)


class NecklaceForm(JewelryCommonForm):
	group = forms.ChoiceField(widget=forms.HiddenInput(), choices=GroupEnum.choices(), initial=GroupEnum.NE.value)
	length = forms.FloatField(required=False, initial=None)  # in cm
	width_max = forms.FloatField(required=False, initial=None)  # in cm
	width_min = forms.FloatField(required=False, initial=None)  # in cm
	isAdjustable = forms.BooleanField(required=False, initial=True)


class RingForm(JewelryCommonForm):
	group = forms.ChoiceField(widget=forms.HiddenInput(), choices=GroupEnum.choices(), initial=GroupEnum.RI.value)
	circumference = forms.FloatField(required=False, initial=None)  # in mm
	width_max = forms.FloatField(required=False, initial=None)  # in cm
	width_min = forms.FloatField(required=False, initial=None)  # in cm
	isAdjustable = forms.BooleanField(required=False, initial=True)


class EarringForm(JewelryCommonForm):
	group = forms.ChoiceField(widget=forms.HiddenInput(), choices=GroupEnum.choices(), initial=GroupEnum.EA.value)
	heigth = forms.FloatField(required=False, initial=None)  # in cm
	width_max = forms.FloatField(required=False, initial=None)  # in cm
	width_min = forms.FloatField(required=False, initial=None)  # in cm


# class JewelryPhotoForm(forms.Form):
# 	photo = forms.ImageField()
# 	priority = forms.DecimalField(min_value=0, max_value=1000)
