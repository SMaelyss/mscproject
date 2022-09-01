from unicodedata import name
from django.urls import path

from . import views
from home.views import homepage
from listall.forms import ListallForm


urlpatterns = [
  path('', views.listall_homepage, name='listall_homepage'),
  path('listall_result', views.listall_result, name='listall_result'),
  
]

