from turtle import home
from django.urls import path

from . import views
from home.views import homepage
from indep.forms import IndepLocForm, IndepIdNameForm

urlpatterns = [
  path('', views.indep_homepage, name='indep_homepage'),
  path('indep_result', views.indep_result, name='indep_result')

]


