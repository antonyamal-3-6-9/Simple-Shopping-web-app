from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['billingName', 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'zip_code', 'phone_number']
        labels = {
            'billingName': 'Billing Name',
            'address_line_1': 'Address Line 1',
            'address_line_2': 'Address Line 2',
            'zip_code': 'Zip Code',
            'phone_number': 'Phone Number'
        }
        widgets = {
            'billingName': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'})
        }
