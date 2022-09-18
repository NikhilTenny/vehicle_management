from django.test import TestCase
from basic.models import Vehicle
from django.contrib.auth import get_user_model
from basic.forms import LoginForm, createForm, EditForm


class TestForms(TestCase):
    def setUp(self):
        self.log_form_data = {
            'username': 'user',
            'password': 'passw'
        }
        self.create_form_data = {
            'number': 'KL17G4433',
            'v_type': '3',
            'model': 'Honda',
            'desc':'A good auto'
        }
        Vehicle.objects.create(**self.create_form_data)
    
    def test_login_form_valid(self):
        form = LoginForm(data=self.log_form_data)
        self.assertTrue(form.is_valid())
    
    def test_create_form(self):
        form = createForm(data=self.create_form_data)
        self.assertFalse(form.is_valid())

