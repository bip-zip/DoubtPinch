from django.test import TestCase
from django.urls import reverse, resolve
from dpapp.views import (Home, Detail, Profile, PostDoubtView, 
Search,CommentView, NotificationView, TagsView, UpdateAnswer, DeleteAnswer)

class TestUrls(TestCase):
    def test_home_url_resloves(self):
        url=reverse('dpapp:home')
        self.assertEqual(resolve(url).func.view_class, Home)
    
    def test_detail_url_resloves(self):
        url=reverse('dpapp:detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, Detail)

    def test_profile_url_resloves(self):
        url=reverse('dpapp:profile')
        self.assertEqual(resolve(url).func.view_class, Profile)

    def test_postdoubt_url_resloves(self):
        url=reverse('dpapp:adddoubt')
        self.assertEqual(resolve(url).func.view_class, PostDoubtView)

    def test_search_url_resloves(self):
        url=reverse('dpapp:search')
        self.assertEqual(resolve(url).func.view_class, Search)

    def test_comment_url_resloves(self):
        url=reverse('dpapp:comment', args=[2])
        self.assertEqual(resolve(url).func.view_class, CommentView)

    def test_notifications_url_resloves(self):
        url=reverse('dpapp:notifications')
        self.assertEqual(resolve(url).func.view_class, NotificationView)
    
    def test_tags_url_resloves(self):
        url=reverse('dpapp:tags', args=['random-slug'])
        self.assertEqual(resolve(url).func.view_class, TagsView)

    def test_updateanswer_url_resloves(self):
        url=reverse('dpapp:update_answer', args=[1])
        self.assertEqual(resolve(url).func.view_class, UpdateAnswer)

    def test_deleteanswer_url_resloves(self):
        url=reverse('dpapp:delete_answer', args=[2])
        self.assertEqual(resolve(url).func.view_class, DeleteAnswer)
    
    


    
    
    

    


