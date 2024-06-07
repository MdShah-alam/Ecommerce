from django import forms
from django.contrib.auth.models import User
from . models import ShippingAddress


class ShippingForm(forms.ModelForm):
    Shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping Full name'}) , required=True)
    Shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping Email Address'}) , required=True)
    Shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping address1'}) , required=True)
    Shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping address2'}) , required=True)
    Shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping city'}) , required=True)
    Shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping state'}) , required=False)
    Shipping_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping zipcode'}) , required=False)
    Shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Shipping country'}) , required=True)
    
    class Meta:
        model = ShippingAddress
        fields = ['Shipping_full_name','Shipping_email','Shipping_address1','Shipping_address2','Shipping_city','Shipping_state','Shipping_zipcode','Shipping_country']
        
        exclude = ['user',]       
                  