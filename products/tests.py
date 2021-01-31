from django.test import TestCase

from .internal.enum import ColorEnum
from .internal.enum import StoneEnum
from .models        import Bracelet

class BraceletTestCase(TestCase):
	def setUp(self):
		Bracelet.objects.create(
			# Common
			title        = "My title",
			brief        = "My brief",
			description  = "My description",
			stone        = StoneEnum.LAPIS_LAZULI,
			macrame      = True,
			pcolor       = ColorEnum.RED,

			# Bracelet
			diameter_max = 2.5,
			diameter_min = 1.5,
			width_max    = 0.8,
			width_min    = 0.3,
			isAdjustable = True
		)

	def test_bracelet_creation(self):
		"""Bracelets are created correctly"""
		bracelet = Bracelet.objects.get(title="My title")
		self.assertEqual(bracelet.title, "My title")


from .internal.enum import MaterialEnum


class MaterialEnumTestCase(TestCase):
	def setUp(self):
		self.a = MaterialEnum.N

	def test_getName(self):
		self.assertEqual(self.a.getName(), "None")

	def test_getId(self):
		self.assertEqual(self.a.getId(), "NO")
