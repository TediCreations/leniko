import random
from django import template

from products.internal.models import JewelryPhoto

register = template.Library()

@register.simple_tag
def getSM():
    r = random.choice([2,2,2,2,3,3,4])
    print( "S<: {}".format(r) )
    return "asasas"


@register.filter(name='thumbUrl')
def thumbUrl(self, mode=None):

	if not isinstance(self, JewelryPhoto):
		raise Exception(f"Only {type(JewelryPhoto)} allowed!")

	url=None
	if self:
		url=self.getPhoto(mode).url
	return url
