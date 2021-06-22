from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from .models import User

class RegisterForm(UserCreationForm):
    # password0 = forms.CharField(widget=forms.PasswordInput)
    # password1 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    # prepopulated_fields = {'username': ('first_name', 'last_name',)}

    class Meta():
        model = User
        fields = ('email', 'first_name', 'last_name')


    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
