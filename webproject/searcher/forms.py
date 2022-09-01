
from turtle import textinput
from typing import Text
from django import forms 

mm_choices = [
  (0.9, '0.9'),
  (0.8, '0.8'),
  (0.7, '0.7'),
  (0.6, '0.6'),
  (0.5, '0.5'),
  (0.4, '0.4'),
]

p_adj_choices = [
  (0.9, '0.9'),
  (0.8, '0.8'),
  (0.7, '0.7'),
  (0.6, '0.6'),
  (0.5, '0.5'),
  (0.4, '0.4'),
]

strand_choices = [
  ('+', '+'),
  ('-', '-'),

]

element_type_choices_nonloc = [
  ('Srna','sRNA'),
  ('Cds','CDS'),
  ('Utr','UTR'),
  ('Annotated_ncrna','Annotated ncRNA'),
]

element_type_choices = [
  ('Srna','sRNA'),
  ('Utr','UTR'),
]

id_name_choices = [
  ('name', 'element name'),
  ('id', 'element id')
]

class SearcherLocForm(forms.Form):
  user_input_start = forms.IntegerField(label='Sequence start ')

  user_input_end = forms.IntegerField(label='Sequence end')

  user_input_strand = forms.ChoiceField(choices= strand_choices, label='Sequence strand')

  user_input_mm = forms.ChoiceField(choices= mm_choices, label='Module match score')

  user_input_p_adj = forms.ChoiceField(choices= p_adj_choices, label='P adjusted correlation score')

  user_input_element_type= forms.ChoiceField(choices= element_type_choices, label='Genome element type', widget=forms.RadioSelect)

class SearcherIdNameForm( forms.Form):

  user_input_element_id = forms.ChoiceField(choices= id_name_choices, label='Element id or name', widget=forms.RadioSelect)

  user_input_text= forms.CharField(label='Text to search', max_length=50)
 
  user_input_mm = forms.ChoiceField(choices= mm_choices, label='Module match score')

  user_input_p_adj = forms.ChoiceField(choices= p_adj_choices, label='P adjusted correlation score')

  user_input_element_type= forms.ChoiceField(choices= element_type_choices_nonloc, label='Genome element type', widget=forms.RadioSelect)
