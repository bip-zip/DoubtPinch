from django.test import TestCase, Client
from accounts.models import User
from dpapp.models import *
class TestModels(TestCase):
        
    def test_total_replies(self):
        user=User.objects.create(email='ok@gmail.com',password='wowow#ds')
        self.doubt=Doubt.objects.create(
            user=user, 
            title='What is django?',
            description='idk what it is'
        )
        self.answer=Answer.objects.create(
            user=user,
            doubt=self.doubt
        )
        self.assertEqual(self.doubt.total_replies, 1)
        

    def test_actual_vote(self): 
        user=User.objects.create(email='ok@gmail.com',password='wowow#ds')
        self.doubt=Doubt.objects.create(
            user=user, 
            title='What is django?',
            description='idk what it is'
        )
        self.answer=Answer.objects.create(
            user=user,
            doubt=self.doubt
        )
        self.right= RightPoint.objects.create(answer=self.answer,user=user)

        self.assertEqual(self.answer.actual_vote, 1)
        

