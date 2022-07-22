"""
File: elements_manipulator.py

Version: V1.2
Date: 04.07.2022
Function: Obtains the list of elements and element types and transform them into sql values format for table insertion.

Author: Sarah Maelyss N'djomon
------------------------------------------------------------------------------------------------------------------------
Description
===========
This file takes a list of all the cds, srna, utr and ncrna element's elemt_ids and element_types and places them into
the values format needed for insertion into the sql element table. This involves surrounding each item by quotations,
separating them with a comma and encompassing them in brackets. Example: ('element_id', 'element_type').

------------------------------------------------------------------------------------------------------------------------
calls all_elements.txt
is called by tables_sql.py

"""
import sys

sys.path.insert(0, "./")
sys.path.insert(0, "../")
sys.path.insert(0, "./datafiles/")


# import and open the file with the element ids and types
all_elements_raw = '/d/projects/u/ns003/MSC_PROJECT_DB/mydb/datafiles/all_elements.txt'

all_elements_list = list()
with open(all_elements_raw, 'r') as f:
    all_elements_list = f.read().split()


# Extract from the opened file, the element ids and element types
counter = 0
element_id_list = []
element_type_list = []
for i in all_elements_list:
    counter += 1
    if counter % 2 != 0:
        element_id_list.append(i)
    else:
        element_type_list.append(i)

# Create dictionary for the element id and element types
em_id = element_id_list # key
em_type = element_type_list # value

zipper = zip(em_id, em_type)
em_dict = dict(zipper)

# Create a variable with the element ids and types in the sql values format
em_fin = str()
for k, v in em_dict.items():
    em_fin = f'{em_fin}(\'{k}\', \'{v}\'),\n'


# Test 
# print(em_fin)





