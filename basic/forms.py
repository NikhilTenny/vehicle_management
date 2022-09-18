from dataclasses import fields
from django import forms
from django.contrib.auth import get_user_model
from basic.models import Vehicle
from django.core.exceptions import ValidationError


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
    number = forms.CharField(widget=forms.TextInput(
        attrs={
        'class': 'form-control',
        }))
    v_type = forms.CharField(widget=forms.Select(choices=Vehicle.types,
        attrs={
        'class': 'form-control',
        }))
    model = forms.CharField(widget=forms.TextInput(
        attrs={
        'class': 'form-control',
        }))
    desc = forms.CharField(widget=forms.Textarea(
        attrs={
        'class': 'form-control',
        'rows': 4, 
        'cols': 30,
        }))
    class Meta:
        model = Vehicle
        fields = ['number', 'v_type', 'model', 'desc']

    # Checking if the giving vehicle number already exists in the database
    def clean_number(self):
        number = self.cleaned_data['number']
        if Vehicle.objects.filter(number=number).exists():
            raise ValidationError("Number already exists")
        return number

class EditForm(forms.ModelForm):
    number = forms.CharField(widget=forms.TextInput(
        attrs={
        'class': 'form-control',
        }))
    v_type = forms.CharField(widget=forms.Select(choices=Vehicle.types,
        attrs={
        'class': 'form-control',
        }))
    model = forms.CharField(widget=forms.TextInput(
        attrs={
        'class': 'form-control',
        }))
    desc = forms.CharField(widget=forms.Textarea(
        attrs={
        'class': 'form-control',
        'rows': 4, 
        'cols': 30,
        }))
    class Meta:
        model = Vehicle
        fields = ['number', 'v_type', 'model', 'desc']




