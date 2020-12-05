import random
from django import template

register = template.Library()

@register.simple_tag
def getSM():
    r = random.choice([2,2,2,2,3,3,4])
    print( "S<: {}".format(r) )
    return "asasas"
