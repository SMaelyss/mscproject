"""
File: home/views.py
Version: V1.3
Date: 010.08.2022
Function: Function to render a home page
Author: Sarah Maelyss N'djomon
------------------------------------------------------------------------------------------------------------------------
Description
===========
Two functions.
homepage renders the home page html
------------------------------------------------------------------------------------------------------------------------
"""




from django.shortcuts import render
from listall.views import listall_homepage
from searcher.views import searcher_homepage

# Create your views here.


def homepage(request):
  return render(request, 'home.html')




  

