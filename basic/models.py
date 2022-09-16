from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class Vehicle(models.Model):
    alpha_numeric = RegexValidator(r'^[0-9a-zA-Z]*$', "Please enter only alphanumeric characters")
    types = (
        ('2','Two Wheeler'),
        ('3','Three Wheeler'),
        ('$','Four Wheeler')
    )

    number = models.CharField(max_length=50, blank=False, validators=[alpha_numeric], unique=True)
    v_type = models.CharField(max_length=1, choices=types)
    model = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.number;

