from django.test import SimpleTestCase
from dpapp.forms import DoubtForm, AnswerForm, CommentForm

class TestForms(SimpleTestCase):

    def test_doubtform_valid(self): 
        form=DoubtForm(data={"title":'is it okay?','description':'assist me?','tags':'mydoubt'})
        self.assertTrue(form.is_valid())
    
    def test_doubtform_isnot_valid(self): 
        form=DoubtForm(data={"title":'','description':'assist me?','tags':'mydoubt'})
        self.assertFalse(form.is_valid())

    def test_answersform_isvalid(self):
        form=AnswerForm(data={'description':'wow'})
        self.assertTrue(form.is_valid())

    def test_answersform_isnot_valid(self):
        form=AnswerForm(data={'description':''})
        self.assertFalse(form.is_valid())

    def test_commentform_isvalid(self):
        form=CommentForm(data={'description':'superb'})
        self.assertTrue(form.is_valid())

    def test_commentform_isnot_valid(self):
        form=CommentForm(data={'description':''})
        self.assertFalse(form.is_valid())

    