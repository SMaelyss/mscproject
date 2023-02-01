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

from searcher.forms import SearcherIdNameForm, SearcherLocForm
from .models import Modules, ModuleCorrelation, Elements, Relations, Samples, GrowthConditions, GoTerms, Srna, Utr, AnnotatedNcrna, Cds
from django.views import View

from django.db.models import Q

# Create your views here.


# Render webpage with two forms
def searcher_homepage(request):
  loc_form = SearcherLocForm()
  id_name_form = SearcherIdNameForm()
  context = {
    'loc_form': loc_form,
    'id_name_form': id_name_form,   
  }
  return render(request, 'searcher.html', context)

def searcher_result(request):
  # obtain user input from form
  id_name_form = SearcherIdNameForm()
  loc_form = SearcherLocForm()

  # variables to be used later on
  context = {}
  template_if = ''
  # check if POST
  if request.method == 'POST':
    id_name_form = SearcherIdNameForm(request.POST)
    loc_form = SearcherLocForm(request.POST)

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
        mm = loc_form.cleaned_data['user_input_mm']
        raw_cor = loc_form.cleaned_data['user_input_raw_cor']
        cor_dir = loc_form.cleaned_data['user_input_cor_direction']
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
          
          # obtain all elements in the same module of the searched element with a module match score of a given amount
          def return_element_network(element_id, mm):
            mm = mm
            module_id = Relations.objects.filter(element_id=element_id).values_list('module_id',flat=True)[0]
            network_element_type = Relations.objects.filter(Q(module_id=module_id) & Q(module_match_score__gt=mm)).values_list('element_type',flat=True)
            network_element_id = Relations.objects.filter(Q(module_id=module_id) & Q(module_match_score__gt=mm)).values_list('element_id',flat=True)
            network_mm = Relations.objects.filter(Q(module_id=module_id) & Q(module_match_score__gt=mm)).values_list('module_match_score',flat=True)

            # if network_zip.count > 50: 
            #   'some kind of warning'
            network_zip = zip(network_element_id, network_element_type, network_mm)
            #print(module_id.query)
            #print(module_id)
            #print(network.query)
            for i in network_mm:
              print(i)
    
         
            return network_zip 
          element_network = return_element_network(element_id, mm)
          
        # obtain all conditions of a given p score in relation to the searched elements module
          def return_module_network(element_id, raw_cor, cor_dir):
          
            raw_cor_mod = str(f"{cor_dir}{raw_cor}")
          

            module_id = Relations.objects.filter(element_id=element_id).values_list('module_id',flat=True)[0]

            network_summed_condition_name = list()

            # Allow users to obtain all item swith correlation score more positive or more negative than threshold.

            if cor_dir == '+':
              if raw_cor == 0:
                network_summed_condition_name = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod, raw_cor__lt=0.5 )).values_list('summed_condition_name', flat=True)
                network_raw_cor = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod,raw_cor__lt=0.5 )).values_list('raw_cor', flat=True)
                network_p_adj = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod,raw_cor__lt=0.5 )).values_list('p_adjusted_cor', flat=True)
              else:
                network_summed_condition_name = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod)).values_list('summed_condition_name', flat=True)
                network_raw_cor = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod)).values_list('raw_cor', flat=True)
                network_p_adj = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod)).values_list('p_adjusted_cor', flat=True)
            elif cor_dir == '-':
              if raw_cor == 0:
                network_summed_condition_name = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod, raw_cor__gte=-0.5)).values_list('summed_condition_name', flat=True)
                network_raw_cor = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod, raw_cor__gte=-0.5)).values_list('raw_cor', flat=True)
                network_p_adj = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod, raw_cor__gte=-0.5)).values_list('p_adjusted_cor', flat=True)
              else:
                network_summed_condition_name = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod)).values_list('summed_condition_name', flat=True)
                network_raw_cor = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod)).values_list('raw_cor', flat=True)
                network_p_adj = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod)).values_list('p_adjusted_cor', flat=True)
        

            network_zip = zip(network_summed_condition_name, network_raw_cor, network_p_adj)

            return network_zip
          module_network = return_module_network(element_id, raw_cor, cor_dir)

          print(module_network)

        # create a vis.js node and edge network of the searched element 
          def vis_network(element_id, element_type, mm):
            module_id = Relations.objects.filter(element_id=element_id).values_list('module_id',flat=True)[0]
            network_element_id = Relations.objects.filter(Q(module_id=module_id) & Q(module_match_score__gt=mm)).values_list('element_id',flat=True)
            network_element_type = Relations.objects.filter(Q(module_id=module_id) & Q(module_match_score__gt=mm)).values_list('element_type',flat=True)

            target_attribute = list(network_element_type)
            target_nodes = list(network_element_id)
            count = 0
            source_attribute = list()
            source_nodes = list()
            while count <  len(target_nodes):
              count += 1
              source_nodes.append(element_id)
              source_attribute.append(element_type)

            if element_type == 'Srna':
              sn1 = Srna.objects.filter(srna_element_id=element_id).values_list('gene_element_id', flat=True)[0]
              source_nodes.append(element_id)
              source_attribute.append(element_type)
              target_nodes.append(sn1)
              target_attribute.append('Cds')

            elif element_type == 'Utr':
              sn1 = Utr.objects.filter(utr_element_id=element_id).values_list('downstream_gene_element_id', flat=True)[0]
              sn12 = Utr.objects.filter(utr_element_id=element_id).values_list('upstream_gene_element_id', flat=True)[0]

        
              source_nodes.append(element_id)
              source_attribute.append(element_type)
              target_nodes.append(sn1)
              target_attribute.append('Cds')

              source_nodes.append(element_id)
              source_attribute.append(element_type)
              target_nodes.append(sn12)
              target_attribute.append('Cds')
          
          
            sn2 = list(network_element_id)
            for id in sn2:
             types = Relations.objects.filter(element_id=id).values_list('element_type',flat=True)[0]
             if types == 'utr':
              sn3 = Utr.objects.filter(utr_element_id=id).values_list('downstream_gene_element_id', flat=True)[0]
              sn4 = Utr.objects.filter(utr_element_id=id).values_list('upstream_gene_element_id', flat=True)[0]
              source_nodes.append(id)
              source_attribute.append(types)
              target_nodes.append(sn3)
              target_attribute.append('cds')
              source_nodes.append(id)
              source_attribute.append(types)
              target_nodes.append(sn4)
              target_attribute.append('cds')
            
             if types == 'srna':
              sn3 = Srna.objects.filter(srna_element_id=id).values_list('gene_element_id', flat=True)[0]
              source_nodes.append(id)
              source_attribute.append(types)
              target_nodes.append(sn3)
              target_attribute.append('cds')

              

              id_count = 0
            return_edge_zip = zip(source_nodes, target_nodes)     
          
          
            return source_nodes, source_attribute, target_nodes, target_attribute , return_edge_zip

          s_nodes = vis_network(element_id, element_type, mm)[0]
          t_nodes = vis_network(element_id, element_type, mm )[2]
          s_attribute = vis_network(element_id, element_type,mm)[1]
          t_attribute = vis_network(element_id, element_type, mm)[3]
          edge_zip = vis_network(element_id, element_type, mm)[4]
        
          all_nodes = s_nodes + t_nodes
          all_attributes = s_attribute + t_attribute
          all_attributes = ['#7BE141' if item == 'utr' else item for item in all_attributes]
          all_attributes = ['#7BE141' if item == 'Utr' else item for item in all_attributes]
          all_attributes = ['#c6637b' if item == 'Srna' else item for item in all_attributes]
          all_attributes = ['#c6637b' if item == 'srna' else item for item in all_attributes]
          all_attributes = ['#8de8e8' if item == 'cds' else item for item in all_attributes]
          all_attributes = ['#8de8e8' if item == 'Cds' else item for item in all_attributes]

          nodes_zip = zip(all_nodes, all_attributes )

         
          if nodes_zip is not None:
             nodes_zip = sorted(set(nodes_zip))
          
          else:
            nodes_zip = ''


          all_nodes =  sorted(set(all_nodes))
    
          t = 'LOCATION SEARCH USED'
          context = {
            'nodes_zip': nodes_zip,
  
            'all_nodes': all_nodes,
            'ez': edge_zip,
            'ti': template_if,
            'module_network': module_network,
            'element_network': element_network,
            'element_id': element_id,
            'start':start,
            'end':end,
            'strand':strand,
            'mm':mm,
            'raw_cor':raw_cor,
            'cor_dir':cor_dir,
            'element_type': element_type,
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
        mm = id_name_form.cleaned_data['user_input_mm']
        raw_cor = id_name_form.cleaned_data['user_input_raw_cor']
        cor_dir = id_name_form.cleaned_data['user_input_cor_direction']
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
          
          return element_id
        element_id = list(return_element_id(id_name, text, element_type))[0]
        
       
        if element_id != 'e':
          def return_element_network(element_id, mm):
            mm = mm
            print(mm)
            module_id = Relations.objects.filter(element_id=element_id).values_list('module_id',flat=True)[0]
            network_element_type = Relations.objects.filter(Q(module_id=module_id) & Q(module_match_score__gt=mm)).values_list('element_type',flat=True)
            network_element_id = Relations.objects.filter(Q(module_id=module_id) & Q(module_match_score__gt=mm)).values_list('element_id',flat=True)
            network_mm = Relations.objects.filter(Q(module_id=module_id) & Q(module_match_score__gt=mm)).values_list('module_match_score',flat=True)
            print(network_element_id)
            

            #if network_zip.count > 50: 
            #  'some kind of warning'
            network_zip = zip(network_element_id, network_element_type, network_mm)
            #print(module_id.query)
            #print(module_id)
            #print(network.query)
            
            return network_zip 
          
          element_network = return_element_network(element_id, mm)
          print(element_id)

          def return_module_network(element_id, raw_cor, cor_dir):
            raw_cor_mod = str(f"{cor_dir}{raw_cor}")
            module_id = Relations.objects.filter(element_id=element_id).values_list('module_id',flat=True)[0]
            print(module_id)

            network_summed_condition_name = list()

            # Allow users to obtain all item swith correlation score more positive or more negative than threshold.
            if cor_dir == '+':
              if raw_cor == 0:
                network_summed_condition_name = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod, raw_cor__lt=0.5 )).values_list('summed_condition_name', flat=True)
                network_raw_cor = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod,raw_cor__lt=0.5 )).values_list('raw_cor', flat=True)
                network_p_adj = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod,raw_cor__lt=0.5 )).values_list('p_adjusted_cor', flat=True)
              else:
                network_summed_condition_name = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod)).values_list('summed_condition_name', flat=True)
                network_raw_cor = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod)).values_list('raw_cor', flat=True)
                network_p_adj = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__gte=raw_cor_mod)).values_list('p_adjusted_cor', flat=True)
            elif cor_dir == '-':
              if raw_cor == 0:
                network_summed_condition_name = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod, raw_cor__gte=-0.5)).values_list('summed_condition_name', flat=True)
                network_raw_cor = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod, raw_cor__gte=-0.5)).values_list('raw_cor', flat=True)
                network_p_adj = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod, raw_cor__gte=-0.5)).values_list('p_adjusted_cor', flat=True)
              else:
                network_summed_condition_name = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod)).values_list('summed_condition_name', flat=True)
                network_raw_cor = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod)).values_list('raw_cor', flat=True)
                network_p_adj = ModuleCorrelation.objects.filter(Q(module_id=module_id) & Q(raw_cor__lte=raw_cor_mod)).values_list('p_adjusted_cor', flat=True)
        

            
            network_zip = zip(network_summed_condition_name, network_raw_cor, network_p_adj)
            

            return network_zip
          module_network = return_module_network(element_id, raw_cor, cor_dir)

          def vis_network(element_id, element_type,mm):
            module_id = Relations.objects.filter(element_id=element_id).values_list('module_id',flat=True)[0]
            network_element_id = list()
            network_element_id = Relations.objects.filter(Q(module_id=module_id) & Q(module_match_score__gt=mm)).values_list('element_id',flat=True)
            
            


            network_element_type = Relations.objects.filter(Q(module_id=module_id) & Q(module_match_score__gt=mm)).values_list('element_type',flat=True)
          

            target_attribute = list(network_element_type)
            target_nodes = list(network_element_id)
            count = 0
            source_attribute = list()
            source_nodes = list()
            while count <  len(target_nodes):
              count += 1
              source_nodes.append(element_id)
              source_attribute.append(element_type)

            # get the related genes elements 
            if element_type == 'Srna':
              sn1 = Srna.objects.filter(srna_element_id=element_id).values_list('gene_element_id', flat=True)[0]
              source_nodes.append(element_id)
              source_attribute.append(element_type)
              target_nodes.append(sn1)
              target_attribute.append('Cds')

            elif element_type == 'Utr':
              sn1 = Utr.objects.filter(utr_element_id=element_id).values_list('downstream_gene_element_id', flat=True)[0]
              sn12 = Utr.objects.filter(utr_element_id=element_id).values_list('upstream_gene_element_id', flat=True)[0]

              source_nodes.append(element_id)
              source_attribute.append(element_type)
              target_nodes.append(sn1)
              target_attribute.append('Cds')

              source_nodes.append(element_id)
              source_attribute.append(element_type)
              target_nodes.append(sn12)
              target_attribute.append('Cds')
            
            elif element_type == 'Annotated_ncrna':
              sn1 = AnnotatedNcrna.objects.filter(annotated_ncrna_element_id=element_id).values_list('related_srna_name', flat=True)[0]
              source_nodes.append(element_id)
              source_attribute.append(element_type)
              target_nodes.append(sn1)
              target_attribute.append('Srna')
            
            types = ''
            
          
          
          
            sn2 = list(network_element_id)
            for id in sn2:
             types = Relations.objects.filter(element_id=id).values_list('element_type',flat=True)[0]
             if types == 'utr':
              sn3 = Utr.objects.filter(utr_element_id=id).values_list('downstream_gene_element_id', flat=True)[0]
              sn4 = Utr.objects.filter(utr_element_id=id).values_list('upstream_gene_element_id', flat=True)[0]
              source_nodes.append(id)
              source_attribute.append(types)
              target_nodes.append(sn3)
              target_attribute.append('cds')
              source_nodes.append(id)
              source_attribute.append(types)
              target_nodes.append(sn4)
              target_attribute.append('cds')
            
             if types == 'srna':
              sn3 = Srna.objects.filter(srna_element_id=id).values_list('gene_element_id', flat=True)[0]
              source_nodes.append(id)
              source_attribute.append(types)
              target_nodes.append(sn3)
              target_attribute.append('cds')
            if types == 'Annotated_ncrna':
              sn3 = AnnotatedNcrna.objects.filter(annotated_ncrna_element_id=id).values_list('related_srna_name', flat=True)[0]
              source_nodes.append(id)
              source_attribute.append(types)
              target_nodes.append(sn3)
              target_attribute.append('srna')

              id_count = 0
            
            return_edge_zip = zip(source_nodes, target_nodes)     
            return source_nodes, source_attribute, target_nodes, target_attribute , return_edge_zip

          s_nodes =vis_network(element_id, element_type,mm )[0]
          t_nodes =vis_network(element_id, element_type, mm)[2]
          s_attribute =vis_network(element_id, element_type,mm)[1]
          t_attribute =vis_network(element_id, element_type,mm)[3]
          edge_zip =vis_network(element_id, element_type,mm)[4]

        
          all_nodes = s_nodes + t_nodes

          
        
       
          all_attributes = s_attribute + t_attribute
          all_attributes = ['#7BE141' if item == 'utr' else item for item in all_attributes]
          all_attributes = ['#7BE141' if item == 'Utr' else item for item in all_attributes]
          all_attributes = ['#c6637b' if item == 'Srna' else item for item in all_attributes]
          all_attributes = ['#c6637b' if item == 'srna' else item for item in all_attributes]
          all_attributes = ['#8de8e8' if item == 'cds' else item for item in all_attributes]
          all_attributes = ['#8de8e8' if item == 'Cds' else item for item in all_attributes]
          all_attributes = ['#f9e099' if item == 'annotated_ncrna' else item for item in all_attributes]
          all_attributes = ['#f9e099' if item == 'Annotated_ncrna' else item for item in all_attributes]

          nodes_zip = zip(all_nodes, all_attributes)
          if nodes_zip is not None:
             nodes_zip = sorted(set(nodes_zip))
          
          else:
            nodes_zip = ''


          

      
             
          
        
          all_nodes =  sorted(set(all_nodes))
          
          

          t = 'ID NAME SEARCH USED'
          context = {
            'nodes_zip': nodes_zip,
            'all_nodes': all_nodes,
            'ez': edge_zip,
            'ti': template_if,
            'module_network': module_network,
            'element_network': element_network,
            'element_id': element_id,
            't':t,
            'id_name':id_name,
            'text':text,
            'mm':mm,
            'raw_cor': raw_cor,
            'cor_dir':cor_dir,
            'element_type': element_type,
          }

          

        else:
          error_text = 'check inputs'
          context = {
            'error_text':error_text,
          }

  else:
    print('not POST')

  return render(request, 'searcher_result.html', context)