"""
Description: Home app, url file
urls for the navigation functions

"""

from django.urls import path

from . import views


urlpatterns = [
  path('', views.homepage, name='home'),
]