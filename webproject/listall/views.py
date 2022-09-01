
"""
File: listall/views.py
Version: V1.4
Date: 05.08.2022
Function: Functions that recieve web requests from a user and returns a webresponse of data from the mysql database
Author: Sarah Maelyss N'djomon
------------------------------------------------------------------------------------------------------------------------
Description
===========
Two functions.
Listall_homepage renders the listall search form on the list all webpage
Listall_result takes the request from the listall form and retrieves the requested data from the database and passes it to the listall_result html.
------------------------------------------------------------------------------------------------------------------------
"""


from multiprocessing import context
from django.shortcuts import render

# import the form
from listall.forms import ListallForm

# Import the model classes (tables from database)
from .models import Modules, ModuleCorrelation, Elements, Relations, Samples, GrowthConditions, GoTerms



# Listall_homepage produces the listall page with the form
def listall_homepage(request):
  form = ListallForm()
  return render(request, 'listall.html', {'form': form})


# Takes input from the form to return the requested data from the model onto a result webpage 'Listall_results'
def listall_result(request):
  form = ListallForm(request.POST) # return the request from  the form
  if request.method == 'POST':
     form = ListallForm(request.POST)
     print('Method is POST') # Is printed in temrinal for testing purposes
     if form.is_valid(): # Validating the form
      listalldata = form.cleaned_data['listalldata'] # Clean the data sent through from the form
      print(listalldata) # Print post request in temrinal for testing purposes
      context = '' # For dynamic webpage

      # if statements to return data depending upon the users request
      if listalldata == 'modules_listall_req': 
        # Obtain data from models related to modules
        m_all =  Modules.objects.all() # objects.all obtains everything in model table
        mc_all = ModuleCorrelation.objects.all() 
        mc_summed_condition_name = ModuleCorrelation.objects.values_list('summed_condition_name', flat=True) 
        # summed condition name is foreign key thus must be obtained as a values list to avoid each object having a pre-fix.
        mc_module = ModuleCorrelation.objects.values_list('module', flat=True) 
        # A foreign key column, flat=True makes sure only object is returned without model name prefix or data type pre-fix
        mc_table_zip = zip(mc_all, mc_summed_condition_name, mc_module) # Create a zip to iterated a for loop in the html page
        #context dict to be called dynamically in the html webpage
        context ={
          'm_all':m_all,
          'mc_table_zip': mc_table_zip,
          'listalldata': listalldata,
        }
        

      elif listalldata == 'elements_listall_req':
        e_id = Elements.objects.values_list('element_id', flat=True)
        e_type = Elements.objects.values_list('element_type', flat=True)
        e_table_zip = zip(e_id, e_type) 

        r_all = Relations.objects.all()
        r_element = Relations.objects.values_list('element', flat=True)
        r_module = Relations.objects.values_list('module', flat=True)
        r_table_zip = zip(r_all, r_element, r_module )

        context ={
          'e_table_zip':e_table_zip,
          'r_table_zip':r_table_zip,
          'listalldata': listalldata,  
        }

      elif listalldata == 'samples_listall_req':
        s_all = Samples.objects.all()
        s_full_con = Samples.objects.values_list('full_condition', flat=True)
        res = Samples.objects.filter(sample_id__in=s_all)
        s_table_zip = zip(s_all, s_full_con)


        gc_full_condition_name = GrowthConditions.objects.values_list('full_condition_name', flat=True)
        gc_full_condition_id = GrowthConditions.objects.values_list('full_condition_id', flat=True)
        gc_table_zip = zip(gc_full_condition_name, gc_full_condition_id)
        context ={
          's_table_zip': s_table_zip,
          'listalldata': listalldata,
          'gc_table_zip':gc_table_zip,
        }

      elif listalldata == 'goterms_listall_req':
        gt_all  = GoTerms.objects.all()
        context ={
          'gt_all':gt_all,
        }

  else:
    print('not POST') # if the request is not post - error handeling, this will not appear on the webpage. 
    # Dynamic context for the wepage to be added later.
    #context = { }
  return render(request, 'listall_result.html', context)




# add valid else






















# Create your views here.

   # render, request the html pg
   # {'title', 'item'}, dict for making the page dynamic, reference in html via '{{title}}'. The 'item' object can come from anywhere, )internet, database etc)
  # render the template, rendering as this will allow the processing of dynamic templates

# makes the form view



#def listall_view(TemplateView):
  #""" code to parse the correct return depending on input """

 # if request.method == 'POST':
#     form = ListallForm(request.POST)
#     if form.is_valid():
#      listall_data_request = form.cleaned_data['listall_data_request']
#      print(listall_data_request)
#      return HttpResponseRedirect('/listall_result')

#  form = ListallForm()
#  return render(request, 'listall.html', {'form': form})


#def listall_result(request):
#  listalldata = request.POST['listall_data_request']
#  res = ''
#  if listalldata == 'modules_listall_req':
#    res = 'module related tables requested'
#  elif listalldata == 'elements_listall_req':
#    res  = 'elements related tables requested'\

#  elif listalldata == 'samples_listall_req':
#    res  = 'samples related tables requested'

#  elif listalldata == 'goterms_listall_req':
 #   res  = 'go terms related tables requested'
  
 # return render(request, 'listall_result.html', {'result': res})
