from django.test import TestCase, Client
from django.urls import reverse
from basic.models import Vehicle
from django.contrib.auth import get_user_model    

class TestLoginView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('login_page')
        self.user = get_user_model()
        self.password = 'fortesting'
        self.credentials = {
            'username': 'testuser',
            'password':'fortesting'
            }
        self.test_user = self.user.objects.create(**self.credentials)
        self.test_user.set_password(self.password)
        self.test_user.is_active = True
        self.test_user.save()



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

    def test_loginView_POST_with_invalid_form(self):
        response = self.client.post(self.url, {
            'password': 'invalidPass'}, 
            follow=True)

        self.assertTemplateUsed(response,'basic/login.html')    




class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse('home_page')
        self.login_url = reverse('login_page')
        self.user = get_user_model()
        self.password = 'fortesting'
        self.credentials = {
            'username': 'testuser',
            'password':'fortesting'
            }
        self.test_user = self.user.objects.create(**self.credentials)
        self.test_user.set_password(self.password)
        self.test_user.is_active = True
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
        self.password = 'fortesting'
        self.credentials = {
            'username': 'testuser',
            'password':'fortesting'
            }
        self.test_user = self.user.objects.create(**self.credentials)
        self.test_user.set_password(self.password)
        self.test_user.is_active = True
        self.test_user.save()
        self.formData = {
            'number': 'KL17G4433',
            'v_type': '3',
            'model': 'Honda',
            'desc':'A good auto'
        }

    
    def test_CreateView_no_user_logged_in(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 302) 

    def test_CreateView_user_logged_in(self):
        # Login a superuser
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
    
    def test_CreateView_POST_user_logged_in(self):
        # Login a superuser
        self.test_user.is_superuser = True
        self.test_user.save()
        self.client.post(self.login_url, self.credentials, follow=True)

        response = self.client.post(self.url, self.formData, follow=True)

        self.assertTemplateUsed(response, 'basic/create.html')
        self.assertEquals('Honda', Vehicle.objects.get(number='KL17G4433').model)

    def test_CreateView_POST_invalid_form(self):
        # Login a superuser
        self.test_user.is_superuser = True
        self.test_user.save()
        self.client.post(self.login_url, self.credentials, follow=True)
        del self.formData['model'] 

        response = self.client.post(self.url, self.formData, follow=True)

        self.assertTemplateUsed(response, 'basic/create.html')
        self.assertEquals(0, Vehicle.objects.all().count())


class TestVechicleView(TestCase):
    def setUp(self):
        self.url = reverse('detail', args='1')
        self.login_url = reverse('login_page')
        self.user = get_user_model()
        self.password = 'fortesting'
        self.credentials = {
            'username': 'testuser',
            'password':'fortesting'
            }
        self.test_user = self.user.objects.create(**self.credentials)
        self.test_user.set_password(self.password)
        self.test_user.is_active = True
        self.test_user.save()
        self.formData = {
            'number': 'KL17G4433',
            'v_type': '3',
            'model': 'Honda',
            'desc':'A good auto'
        }
        Vehicle.objects.create(**self.formData)

    def test_VehicleView_valid_id(self):
        #Login a user
        self.client.post(self.login_url, self.credentials, follow=True)

        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic/detail.html')
    
    def test_VehicleView_invalid_id(self):
        #Login a user
        self.client.post(self.login_url, self.credentials, follow=True)

        response = self.client.get('home/10')

        self.assertEquals(response.status_code, 404)

class TestVechicleEditView(TestCase):
    def setUp(self):
        self.login_url = reverse('login_page')
        self.user = get_user_model()
        self.password = 'fortesting'
        self.credentials = {
            'username': 'testuser',
            'password': self.password
            }
        self.test_user = self.user.objects.create(**self.credentials)
        self.test_user.set_password(self.password)
        self.test_user.is_active = True
        self.test_user.save()
        self.formData = {
            'number': 'KL17G4433',
            'v_type': '3',
            'model': 'Honda',
            'desc':'A good auto'
        }
        Vehicle.objects.create(**self.formData)

    def test_VechicleEditView_normal_user(self):
        #Login a user
        self.client.post(self.login_url, self.credentials, follow=True)

        response = self.client.get(reverse('edit', args='1'))

        self.assertEquals(response.status_code, 403)
    

    def test_VechicleEditView_POST(self):
        #Login a user
        self.test_user.is_staff = True
        self.test_user.save()
        self.client.post(self.login_url, self.credentials, follow=True)
        self.formData['number'] = 'KL17G000'

        response = self.client.post(reverse('edit', args='1'), self.formData)

        self.assertEquals(response.status_code, 302)

    
class TestVechicleDeleteView(TestCase):
    def setUp(self):
        self.login_url = reverse('login_page')
        self.user = get_user_model()
        self.password = 'fortesting'
        self.credentials = {
            'username': 'testuser',
            'password': self.password
            }
        self.test_user = self.user.objects.create(**self.credentials)
        self.test_user.set_password(self.password)
        self.test_user.is_active = True
        self.test_user.save()
        self.formData = {
            'number': 'KL17G4433',
            'v_type': '3',
            'model': 'Honda',
            'desc':'A good auto'
        }
        Vehicle.objects.create(**self.formData)

    def test_VechicleDeleteView_superuser(self):
        #Login a superuser
        self.test_user.is_superuser = True
        self.test_user.save()
        self.client.post(self.login_url, self.credentials, follow=True)

        response = self.client.post(reverse('delete', args='1'))

        self.assertEquals(response.status_code, 302)

    def test_VechicleDeleteView_not_superuser(self):
        #Login a user
        self.client.post(self.login_url, self.credentials, follow=True)

        response = self.client.post(reverse('delete', args='1'))

        self.assertEquals(response.status_code, 403)









