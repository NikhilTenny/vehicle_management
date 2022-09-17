from http import client
from pydoc import resolve
from django.test import TestCase, Client
from django.urls import reverse
from basic.models import Vehicle
from django.contrib.auth import get_user_model    

class TestLoginView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('login_page')
        self.user = get_user_model()
        self.credentials = {
            'username': 'testuser',
            'password': 'fortesting'}
        self.test_user = self.user.objects.create(**self.credentials)


    def test_loginView_GET(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic/login.html')

    def test_loginView_POST_with_valid_credentials(self):
        response = self.client.post(self.url, self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response,'basic/home.html')
    
    def test_loginView_POST_with_invalid_credentials(self):
        response = self.client.post(self.url, {
            'username':'invalidusername',
            'password': 'invalidPass'}, 
            follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response,'basic/login.html')    


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse('home_page')
        self.login_url = reverse('login_page')
        self.user = get_user_model()
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'fortesting'}
        self.test_user = self.user.objects.create(**self.credentials)
        self.test_user.save()

    def test_homeView_user_logged_in(self):
        # Login a user
        self.client.post(self.login_url, self.credentials, follow=True)        
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'basic/home.html')
        self.assertEquals(response.status_code, 200)  

    def test_homeView_no_user_logged_in(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)  


class TestCreateView(TestCase):

    def setUp(self):
        self.url = reverse('create')
        self.login_url = reverse('login_page')
        self.user = get_user_model()
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'fortesting'
            }
        self.test_user = self.user.objects.create(**self.credentials)
        self.test_user.save()
    
    def test_CreateView_no_user_logged_in(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302) 

    def test_CreateView_user_logged_in(self):
        # Login a user
        self.test_user.is_superuser = True
        self.test_user.save()
        self.client.post(self.login_url, self.credentials, follow=True)  
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'basic/create.html')
        self.assertEquals(response.status_code, 200) 

    def test_CreateView_user_not_superuser(self):
        # Login a user
        self.client.post(self.login_url, self.credentials, follow=True)  
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 403) 
