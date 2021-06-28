from django.conf.urls import url
from .views import *
from django.urls import path,include
from .views import Home,Detail, Profile,PostDoubtView, Search


app_name='dpapp'

urlpatterns=[
    
    path('home/', Home.as_view(), name='home'),
    path("detail/<int:id>", Detail.as_view(), name="detail"),
    path('profile/',Profile.as_view(),name='profile'),
    path('adddoubt/',PostDoubtView.as_view(),name='adddoubt'),
    path('saverpoint/',saveRPoint,name='save-rpoint'),
    path('savewpoint/',saveWPoint,name='save-wpoint'),
    path('search/',Search.as_view(),name='search'),
  

]