from ast import arg
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from ..views import (loginView, 
    homeView, 
    CreateView,
    VehicleView,
    VehicleEditView,
    VehicleDeleteView)

class TestUrls(SimpleTestCase):
    
    def test_loginView_url(self):
        url = reverse('login_page')
        self.assertEquals(resolve(url).func, loginView)

    def test_homeView_url(self):
        url = reverse('home_page')
        self.assertEquals(resolve(url).func.view_class, homeView)
    
    def test_CreateView_url(self):
        url = reverse('create')
        self.assertEquals(resolve(url).func.view_class, CreateView)
        
    def test_VehicleView_url(self):
        url = reverse('detail',args=['3'])
        self.assertEquals(resolve(url).func.view_class, VehicleView)

    def test_VehicleEditView_url(self):
        url = reverse('edit',args=['3'])
        self.assertEquals(resolve(url).func.view_class, VehicleEditView)
    
    def test_VehicleDeleteView_url(self):
        url = reverse('delete',args=['3'])
        self.assertEquals(resolve(url).func.view_class, VehicleDeleteView)





