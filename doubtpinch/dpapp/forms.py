from django import forms
from .models import Doubt, Answer, Comment
from accounts.models import User

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.forms import Textarea

class DoubtForm(forms.ModelForm):
    # password1 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    # prepopulated_fields = {'username': ('first_name', 'last_name',)}

    class Meta():
        model = Doubt
        fields = ('title', 'description','tags')
        widgets = {
            # 'description': SummernoteInplaceWidget()
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
            "title": Textarea(attrs={"rows":4, "cols":20}),
            "tags": Textarea(attrs={"rows":4, "cols":20,"placeholder": "Include tags like: python, django, java"}),

        }


class AnswerForm(forms.ModelForm):
    # password1 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    # prepopulated_fields = {'username': ('first_name', 'last_name',)}

    class Meta():
        model = Answer
        fields = ('description',)
        widgets = {
            # 'description': SummernoteInplaceWidget()
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '100px', "placeholder": "Your Solution..."}}),
        }


class CommentForm(forms.ModelForm):
    # password1 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    # prepopulated_fields = {'username': ('first_name', 'last_name',)}

    class Meta():
        model = Comment
        fields = ('description',)
        widgets = {
            # 'description': SummernoteInplaceWidget()
            'description': Textarea(attrs={"rows":3, "cols":20,"placeholder": "Reply with a comment."}),
        }

class ProfileForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('profile_pic',)
        # widgets = {
        #     # 'description': SummernoteInplaceWidget()
        #     'description': Textarea(attrs={"rows":3, "cols":20,"placeholder": "Reply with a comment."}),
        # }