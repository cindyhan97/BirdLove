from urllib import response
from django.test import TestCase, Client
from .models import *
from django.contrib.auth import get_user_model
# Create your tests here.
from django.contrib import auth

class anonTest(TestCase):
    def test_login(self):
        login_data = {'username': 'qwe', 'password': 'qwe123'}
        response = self.client.post('/login', data = login_data)
        self.assertEqual(response.status_code, 200)
    def test_register(self):
        regis_Data = {
        'username':'testname',
        'email':'test@django.com',
        'first_name': 'test_first',
        'last_name':'test_lst',
        'password1':'123456',
        'password2':'123456',
        }
        response = self.client.post('/registration', data = regis_Data)
        self.assertTemplateUsed(response, 'birduser/registration.html')
        self.assertEqual(response.status_code, 200)
        

    def testRightInput_report(self):
        help_data = {
            'nickname': 'testnickname',
            'phoneNumber':"3525253",
            'area':'north',
            'postalCode' :'24124',
            'address1':'testaddress',
            'address2':'testAddress3',
            'upload-1':'image/imageTest.jpg',
            'resuceDescription': 'testresuceDescription'
        }
        response = self.client.post('/help', data = help_data)
        self.assertEqual(response.status_code, 200)


class signedTest(TestCase):
    def setUp(self):
        super(signedTest, self).setUp()
        self.client = Client(enforce_csrf_checks=True)
        self.user = User.objects.create_user(username='testuser', password = 'testpassword')
        self.user.save()
        self.client.login(username='testuser', password='testpassword')
 
    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'birduser/index.html')

    def test_profile(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'birduser/userProfile.html')
        # addressCount = address.objects.all()
        # self.assertEqual(addressCount.count(), 1)

    def testRescueRequest(self):
        help_data = {
            'phoneNumber':"3525253",
            'area':'north',
            'postalCode' :'24124',
            'address1':'testaddress',
            'address2':'testAddress3',
            'upload-1':'image/imageTest.jpg',
            'resuceDescription': 'testresuceDescription'
        }
        response = self.client.post('/help', data = help_data)
        self.assertEqual(response.status_code, 200)
    def adoptionTest(self):
        bird_Data = {
            'name':'testbird',
            'species': 'testspecies',
            'age':'12',
            'adoptDescription': 'testadoptDescription',
            'upload-1':'image/imageTest.jpg',
        }
        response = self.client.post('/adopt', data = bird_Data)
        self.assertEqual(response.status_code, 200)
    def galleryTest(self):
        response = self.client.get('/gallery')
        self.assertEqual(response.status_code, 200)
    def DonationTest(self):
        response = self.client.get('/donate')
        self.assertEqual(response.status_code, 200)