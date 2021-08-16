from django.http import HttpResponse, request
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from .auth import unauthenticated_user
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse


def userlogout(request):
    logout(request)
    return redirect('/')



from django.shortcuts import render
from django.views.generic import TemplateView, View
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import Skill, User, UserSkill
from django.conf import settings
from django.http import HttpResponse





class UserLogoutView(LogoutView):
    success_url = reverse_lazy('accounts:home')
    template_name = 'logged_out'

class UserSignin(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/signup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'signup_active':'active'})
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #set user to inactive until the email confirmation is sent
            # user = request.user
            user.is_active = False
            user.save()
            #send confirmation email
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('accounts/account_activate_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':default_token_generator.make_token(user),
            })
            print(message)
            user.email_user(subject, message, from_email=None, **kwargs)
            messages.success(request, 'Please confirm your email to complete accounts')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form':form})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64)).decode()
            user = User.objects.get(id=uid)
            # print(uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
     

        if user is not None and default_token_generator.check_token(user, token):
            # obj, created = User.objects.get_or_create(user=user)
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request,('Your account have been confirmed.'))
            return redirect('accounts:login')
        else:
            # messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            # return redirect('accounts:activation_invalid')
            return HttpResponse ('The confirmation link was invalid, possibly because it has already been used.')

def activation_sent_view(request):
    return render(request,'accounts/activation_sent.html')

def activation_invalid_view(request):
    return render(request,'accounts/activation_invalid.html')

from django.http import JsonResponse

def validate_user(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email, email_confirmed=True).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this email already exists.'
    return JsonResponse(data)

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

class PasswordReset(View):
    def get(self,request):
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})


    def post(self, request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
            messages.error(request, 'No account was registered with this email.')
            return redirect('accounts:password_reset')
            
            
class UserDesc(View):
    def post(self,request,*args, **kwargs):
        a_user=self.request.user
        desc=request.POST.get('desc')
        print(desc)
        a_user.description=desc
        
        a_user.save()
        return redirect('dpapp:profile')


class SkillUser(View):
    def post(self,request,*args, **kwargs):
        a_user=self.request.user
        level=request.POST.get('level')
        skill_id =request.POST.get('skill')
        print(level,skill_id)
        skill=Skill.objects.get(skill=skill_id)
        UserSkill.objects.create(user=a_user, skill=skill, level=level )
        return redirect('dpapp:profile')

class DeleteSkill(View):
    def get(self,request,*args, **kwargs):
        skill_id=self.kwargs['id']
        UserSkill.objects.get(id=skill_id).delete()
        return redirect('dpapp:profile')


