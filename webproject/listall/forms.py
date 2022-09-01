from django import forms 


#iterables
listall_choices = [
  ('modules_listall_req', 'Modules'),
  ('elements_listall_req', 'Elements'),
  ('samples_listall_req', 'Samples'),
  ('goterms_listall_req', 'Go terms'),
]


# List all form
class ListallForm(forms.Form):
  listalldata = forms.ChoiceField(choices= listall_choices, label= 'Data request')
