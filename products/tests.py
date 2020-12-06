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
			stone        = StoneEnum.LL,
			macrame      = True,
			color        = ColorEnum.RED,

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
