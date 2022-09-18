from django.test import TestCase
from basic.models import Vehicle
from django.contrib.auth import get_user_model
from basic.forms import LoginForm, createForm, EditForm

class TestModel(TestCase):
    def setUp(self):
        self.user = get_user_model()
        self.formData = {
            'number': 'KL17G4433',
            'v_type': '3',
            'model': 'Honda',
            'desc':'A good auto'
        }
    
    def test_model(self):
        obj = Vehicle.objects.create(**self.formData)

        self.assertEquals(str(obj),self.formData['number'])
        
