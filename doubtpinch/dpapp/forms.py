from django import forms
from .models import Doubt, Answer
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class DoubtForm(forms.ModelForm):
    # password1 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    # prepopulated_fields = {'username': ('first_name', 'last_name',)}

    class Meta():
        model = Doubt
        fields = ('title', 'description')
        widgets = {
            # 'description': SummernoteInplaceWidget()
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
        }


class AnswerForm(forms.ModelForm):
    # password1 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    # prepopulated_fields = {'username': ('first_name', 'last_name',)}

    class Meta():
        model = Answer
        fields = ('description',)
        widgets = {
            # 'description': SummernoteInplaceWidget()
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}),
        }


    
