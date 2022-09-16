from dataclasses import fields
from django import forms

from basic.models import Vehicle


class LoginForm(forms.Form): 
    username = forms.CharField(widget=forms.TextInput(
    attrs={
    'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(
    attrs={
    'class': 'form-control',
    }))

# Form to create a new record in vehicle model
class createForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['number', 'v_type', 'model', 'desc']




