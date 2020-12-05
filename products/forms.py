from django import forms
#from .models import Product


class ProductForm(forms.Form):
    # Basic information
    title       = forms.CharField()
    #brief       = forms.TextField(blank=True, null=True)
    #photo       = forms.ImageField(upload_to='static/uploads/', default='static/img/tedi.png')
    #description = forms.TextField(blank=True, null=True)

    # Shop
    #featured    = forms.BooleanField()
    #price       = forms.DecimalField()
    #group       = EnumChoiceField(GroupEnum, default=GroupEnum.N)
    #quantity    = forms.DecimalField()

    # Material
    #metal       = EnumChoiceField(MetalEnum, default=MetalEnum.N)
    #platting    = EnumChoiceField(PlattingEnum, default=PlattingEnum.N)
    #macrame     = forms.BooleanField()
