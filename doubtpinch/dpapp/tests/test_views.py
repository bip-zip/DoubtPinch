from django.test import TestCase, Client,RequestFactory
from django.urls import reverse
from dpapp.models import *
from dpapp.views import Home, Profile
from accounts.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='cody', email='codecharm@softwarica.edu.np', password='top_secret')
        
    def test_home_ofanonymous_GET(self):
        response= self.client.get(reverse('dpapp:home'))
        self.assertRedirects(response, '/?next=/app/home/')

    def test_home(self):
        request = self.factory.get(reverse('dpapp:home'))
        request.user = self.user
        response = Home.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        request = self.factory.get(reverse('dpapp:profile'))
        request.user = self.user
        response = Profile.as_view()(request)
        self.assertEqual(response.status_code, 200)

 

    

    
        
    


        

    
        

