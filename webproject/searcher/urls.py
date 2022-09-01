from turtle import home
from django.urls import path

from . import views
from home.views import homepage
from searcher.forms import SearcherIdNameForm, SearcherLocForm

urlpatterns = [
  path('', views.searcher_homepage, name='searcher_homepage'),
  path('searcher_result', views.searcher_result, name='searcher_result')


]


