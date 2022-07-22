
"""
File: annotated_ncrna_insertinto.py

Version: V1.1
Date: 03.07.2022
Function: annotated_ncrna table items from research data excel file, formatted for sql in MrDataConverter:
ref: https://shancarter.github.io/mr-data-converter/.

Author: Sarah Maelyss N'djomon
------------------------------------------------------------------------------------------------------------------------
Description
===========
This file provides a variable containing the insert into function for populating the annotated_ncrna table.

------------------------------------------------------------------------------------------------------------------------

is called by tables_sql.py

"""


values = """ INSERT INTO annotated_ncrna
  (annotated_ncrna_element_id,annotated_ncrna_name,related_srna_name) 
VALUES 
  ('EBG00000313378','F6','ncRv10243A'),
  ('EBG00000313327','mcr19','ncRv0485'),
  ('EBG00000313383','B55','ncRv10609A'),
  ('EBG00000313364','ASdes','ncRv0824'),
  ('EBG00000313344','mpr5','ncRv11051'),
  ('EBG00000313338','MTS0858','ncRv1092c'),
  ('EBG00000313317','mcr10','ncRv1157'),
  ('EBG00000313387','ncrMT1234','ncRv11196'),
  ('EBG00000313390','mpr6','ncRv1222'),
  ('EBG00000313343','mcr11','ncRv11264c'),
  ('EBG00000313377','mcr3','ncRv11315A'),
  ('EBG00000313340','mcr15','ncRv1364c'),
  ('EBG00000313353','MTS1082','ncRv11373'),
  ('EBG00000313337','G2','ncRv11689c'),
  ('EBG00000313388','AS1726','ncRv1726c'),
  ('EBG00000313376','MTS1338','ncRv11733A'),
  ('EBG00000313322','AS1890','ncRv1890'),
  ('EBG00000313323','ASpks','ncRv2048'),
  ('EBG00000313321','mcr5','ncRv2175c'),
  ('EBG00000313389','mcr16','ncRv2243c'),
  ('EBG00000313380','mcr7','ncRv0024'),
  ('EBG00000313368','mpr11','ncRv12560'),
  ('EBG00000313313','mpr12','ncRv12562'),
  ('EBG00000313367','mpr17','ncRv13596'),
  ('EBG00000313385','mpr18','ncRv13651'),
  ('EBG00000313324','B11','ncRv13660c'),
  ('EBG00000313318','MTS2823','ncRv13661'),
  ('EBG00000313354','C8','ncRv13722Ac'),
  ('EBG00000313356','ncrMT3949','ncRv3842'),
  ('EBG00000313375','MTS2975','ncRv13943');
"""
