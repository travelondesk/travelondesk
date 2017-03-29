from django import forms
from .models import ServiceTicket, DemandTicket, Country
from django.contrib.auth.models import User

class ServiceTicketForm(forms.ModelForm):
    img = forms.ImageField(required=False, widget=forms.FileInput)
    class Meta:
        model = ServiceTicket
        fields = ('name', 'description', 'phone', 'coast', 'latitude', 'longitude', 'country', 'countryShort','region', 'city', 'place', 'img', 'email', 'state', 'category')

class DemandTicketForm(forms.ModelForm):
    img = forms.ImageField(required=False, widget=forms.FileInput)
    class Meta:
        model = DemandTicket
        fields = ('name', 'description', 'phone', 'coast', 'latitude', 'longitude', 'country', 'countryShort', 'region', 'city', 'place', 'img', 'email', 'state', 'category')

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('name', 'intName')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        field = ('first_name', 'last_name')  
        exclude = ('email', 'username', 'password', 'last_login', 'date_joined')
        
class ContactForm(forms.Form):
    subject = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-control'}), max_length = 100)
    sender = forms.EmailField(widget = forms.TextInput(attrs = {'class': 'form-control'}))
    message = forms.CharField(widget = forms.Textarea(attrs = {'class': 'form-control'}))
    copy = forms.BooleanField(required = False)