from django.conf.urls import url
from .views import *
from django.urls import path,include
from .views import UserSignin,ActivateAccount,UserDesc
from django.contrib.auth.views import LogoutView, LoginView


app_name='accounts'

urlpatterns=[
    path('', LoginView.as_view(template_name="accounts/login.html"), name='login'),
    # path('', LoginView.as_view(template_name="accounts/login.html",redirect_authenticated_user=True), name='login'),
    path('signup/', UserSignin.as_view(), name='signup'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('activate/<str:uidb64>/<str:token>',ActivateAccount.as_view(),name='activate'),
    path('sent/', activation_sent_view, name='sent'),
    path('invalid',activation_invalid_view, name='invalid'),
    path('validate_username', validate_user, name='validate_user'),

    path("password_reset", PasswordReset.as_view(), name="password_reset"),
    path("user-desc", UserDesc.as_view(), name="user_desc"),
    path("user-skill", SkillUser.as_view(), name="user_skill"),

    



    

]