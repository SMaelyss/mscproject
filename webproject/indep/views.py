
"""
File: listall/views.py
Version: V1.8
Date: 24.08.2022
Function: Functions that recieve web requests from a user and returns a webresponse of data from the mysql database
Author: Sarah Maelyss N'djomon
------------------------------------------------------------------------------------------------------------------------
Description
===========
Two functions.
Searcher_homepage renders the searcher form on the search webpage
searcher_result takes the request from the searcher form and retrieves the requested data from the database and passes it to the searcher_result html.
------------------------------------------------------------------------------------------------------------------------
"""


from ctypes.wintypes import INT
import email
import re

from django.shortcuts import render
from multiprocessing import context
from django.db import connection

from indep.forms import IndepLocForm, IndepIdNameForm
from .models import Modules, ModuleCorrelation, Elements, Relations, Samples, GrowthConditions, GoTerms, Srna, Utr, AnnotatedNcrna, Cds
from django.views import View

from django.db.models import Q
from django.shortcuts import render

# Create your views here.
def indep_homepage(request):
  loc_form = IndepLocForm()
  id_name_form = IndepIdNameForm()
  context = {
    'loc_form': loc_form,
    'id_name_form': id_name_form,   
  }
  return render(request, 'indep.html', context)


def indep_result(request):
  # obtain user input from form
  id_name_form = IndepIdNameForm()
  loc_form = IndepLocForm()

  # variables to be used later on
  context = {}
  template_if = ''
  # check if POST
  if request.method == 'POST':
    id_name_form = IndepIdNameForm(request.POST)
    loc_form = IndepLocForm(request.POST)

    # Check type of form used, if loc, the element of interest is identified using its location and the element id must be obtained, else, the user entered the element id themselves
    template_if = 'loc'
    if 'loc_searcher_submit' in request.POST:
      print('loc search type') # Prints in terminal for testing purposes
      # Check if form is valid
      if loc_form.is_valid():
        print('loc form is valid')
        start =int(loc_form.cleaned_data['user_input_start'])
        end = int(loc_form.cleaned_data['user_input_end'])
        strand = str(loc_form.cleaned_data['user_input_strand'])
        element_type = loc_form.cleaned_data['user_input_element_type']
        

        # obtain the element id
        def return_element_id(element_type, start, end, strand):
          element_id = ''
          if element_type == 'Srna':
            element_id = list(Srna.objects.filter(Q(seq_start=start) & Q(seq_end=end) & Q(strand=strand)).values_list(flat=True))
          elif element_type == 'Utr':
            element_id = list(Utr.objects.filter(Q(seq_start=start) & Q(seq_end=end) & Q(strand=strand)).values_list(flat=True))

          if not element_id:
            element_id = list('e')

          return element_id
        
        element_id = return_element_id(element_type, start, end, strand)[0]

        # Check an element id was found for error handeling
        if element_id != 'e': 
          
          def return_details(element_id,  element_type):
            
            module_id = ''
            module_id = Relations.objects.filter(element_id=element_id).values_list('module_id',flat=True)[0]
            mm = Relations.objects.filter(element_id=element_id).values_list('module_match_score',flat=True)[0]

            top_conditions = ModuleCorrelation.objects.filter(module_id=module_id).order_by('raw_cor').values_list('summed_condition_name', flat=True)[:3]

            all_details = ''
            if element_type == 'Srna':
              all_details = Srna.objects.filter(srna_element_id=element_id).values()
            else:
              all_details = Utr.objects.filter(utr_element_id=element_id).values()

            return all_details, mm, module_id, top_conditions
          
          module_id = return_details(element_id,  element_type)[2]
          mm = return_details(element_id, element_type)[1]
          top_conditions = return_details(element_id,  element_type)[3]
          all_details = return_details(element_id, element_type)[0]
   
          t = 'LOCATION SEARCH USED'
          context = {
            'ti': template_if,
            'element_id': element_id,
            'element_type': element_type,
            'mm':mm,
            'module_id': module_id,
            'top_conditions': top_conditions,
            'all_details': all_details,
          }

          print(connection.queries)
        else:
          error_text = 'check inputs'
          context = {
            'error_text':error_text,
          }


    
    elif 'id_name_searcher_submit' in request.POST:
      print('id name search type')
      template_if = 'id or name'
      if id_name_form.is_valid():
        print('id name form is valid')
        id_name = id_name_form.cleaned_data['user_input_element_id']
        text = id_name_form.cleaned_data['user_input_text']
       
        element_type = id_name_form.cleaned_data['user_input_element_type']

        def return_element_id(id_name, text, element_type):
          text = str(text)
          element_id = ''
          if id_name == 'id':
            if element_type == 'Srna':
              element_id = Srna.objects.filter(srna_element_id=text).values_list('srna_element_id', flat=True)
            elif element_type == 'Utr':
              element_id = list(Utr.objects.filter(utr_element_id=text).values_list('utr_element_id', flat=True))
            elif element_type == 'Cds':
              element_id = list(Cds.objects.filter(cds_element_id=text).values_list('cds_element_id', flat=True))
            elif element_type == 'Annotated_ncrna':
              element_id = list(AnnotatedNcrna.objects.filter(annotated_ncrna_element_id=text).values_list('annotated_ncrna_element_id', flat=True))
          

          else:
            if element_type == 'Srna':
              element_id = list(Srna.objects.filter(srna_name=text).values_list('srna_element_id', flat=True))
              
            elif element_type == 'Utr':
              element_id = list(Utr.objects.filter(predicted_utr_name=text).values_list('utr_element_id', flat=True))
            elif element_type == 'Cds':
              element_id = list(Cds.objects.filter(cds_name=text).values_list('cds_element_id', flat=True))
            elif element_type == 'Annotated_ncrna':
              element_id = list(AnnotatedNcrna.objects.filter(annotated_ncrna_name=text).values_list('annotated_ncrna_element_id', flat=True))
          

          if not element_id:
            element_id = list('e')
          print(element_id)
          print(connection.queries)
          return element_id
        element_id = list(return_element_id(id_name, text, element_type))[0]
        
        print(element_id)
        if element_id != 'e':
          def return_details(element_id,  element_type):
            
            module_id = ''
            module_id = Relations.objects.filter(element_id=element_id).values_list('module_id',flat=True)[0]
            mm = Relations.objects.filter(element_id=element_id).values_list('module_match_score',flat=True)[0]

            top_conditions = ModuleCorrelation.objects.filter(module_id=module_id).order_by('raw_cor').values_list('summed_condition_name', flat=True)[:3]
            print()

            all_details = ''
            if element_type == 'Srna':
              all_details = Srna.objects.filter(srna_element_id=element_id).values()
            elif element_type == 'Utr':
              all_details = Utr.objects.filter(utr_element_id=element_id).values()
            elif element_type == 'Cds':
              all_details = Cds.objects.filter(cds_element_id=element_id).values()
            elif element_type == 'Annotated_ncrna':
              all_details = AnnotatedNcrna.objects.filter(annotated_ncrna_element_id=element_id).values()


            return all_details, mm, module_id, top_conditions

          
          
          module_id = return_details(element_id,  element_type)[2]
          mm = return_details(element_id, element_type)[1]
          top_conditions = return_details(element_id,  element_type)[3]
          all_details = return_details(element_id, element_type)[0]
   
          t = 'LOCATION SEARCH USED'
          context = {
            'ti': template_if,
            'element_id': element_id,
            'element_type': element_type,
            'mm':mm,
            'module_id': module_id,
            'top_conditions': top_conditions,
            'all_details': all_details,
            }
          
      else:
        error_text = 'check inputs'
        context = {
          'error_text':error_text,
        }

  else:
    print('not POST')

  return render(request, 'indep_result.html', context)