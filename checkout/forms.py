from django import forms

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
	('CA', 'Card'),
	('BD', 'Bank Deposit'),
	('BD', 'Bank Deposit'),
	('CW', 'Click away')
)


class BillingForm(forms.Form):

	billing_address = forms.CharField(required=False)
	billing_address2 = forms.CharField(required=False)
	billing_country = CountryField(blank_label='(select country)').formfield(
		required=False,
		widget=CountrySelectWidget(attrs={
			'class': 'custom-select d-block w-100',
		}))
	billing_zip = forms.CharField(required=False)

	same_billing_address = forms.BooleanField(required=False)


class ShippingForm(forms.Form):

	shipping_address = forms.CharField(required=False)
	shipping_address2 = forms.CharField(required=False)
	shipping_country = CountryField(blank_label='(select country)').formfield(
		required=False,
		widget=CountrySelectWidget(attrs={
			'class': 'custom-select d-block w-100',
		}))
	shipping_zip = forms.CharField(required=False)
