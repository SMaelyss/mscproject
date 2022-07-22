"""
File: tables_sql.py

Version: V1.1
Date: 03.07.2022
Function: Creates tables in database and updates with parsed items

Author: Sarah Maelyss N'djomon
------------------------------------------------------------------------------------------------------------------------
Description
===========
Creates tables in database and updates with parsed items

------------------------------------------------------------------------------------------------------------------------

"""

import sys
sys.path.insert(0, "../")
sys.path.insert(0, "./datafiles/")


# import pymysql and connect to db
import pymysql.cursors
dbname = "ns003"
dbhost = "thoth.cryst.bbk.ac.uk"
dbuser = "ns003"
dbpass = "gly36val28"
dbport = 3306

db = pymysql.connect(host=dbhost, port=dbport, user=dbuser, db=dbname, passwd=dbpass)
cursor = db.cursor()


# imported data files
import elements_manipulator as em  # done
import srna_insertinto as si  # done
import utr_insertinto as ui  # done
import annotated_ncrna_insertinto as ni  # done
import cds_insertinto as ci  # done
import go_term_insertinto as gti  # done
import relations_insertinto as ri  # done
import module_cor_insertinto as mci


# All tables to be made for the database
tables_list = ('samples;','growth_conditions;','module_correlation;','summed_growth_conditions;',
               'relations;','modules;', 'annotated_ncrna;','utr;', 'srna;','go_terms;', 'cds;','elements;', )

# Create, index and populate the summed growth conditions table
sql0 = """CREATE TABLE summed_growth_conditions(
    summed_condition_id INT AUTO_INCREMENT PRIMARY KEY,
    summed_condition_name VARCHAR(190) NOT NULL );  """

sql1 = """CREATE INDEX summed_condition_name_fk
ON summed_growth_conditions(summed_condition_name); """

sql2 = """ INSERT INTO summed_growth_conditions
  (summed_condition_name) 
VALUES 
  ('ammonium'),
  ('histidine'),
  ('lysine'),
  ('hypoxia'),
  ('extended hypoxia'),
  ('reaerated culture'),
  ('exponential'),
  ('butyrate'),
  ('butyrate and glucose'),
  ('glucose'),
  ('high iron'),
  ('low iron'),
  ('acid'),
  ('cholesterol'),
  ('stationary'); """

# Create and populate the growth conditions table
sql3 = """ CREATE TABLE growth_conditions(
full_condition_id INT,
full_condition_name VARCHAR(190) NOT NULL,
summed_condition_name VARCHAR(190),
PRIMARY KEY (full_condition_id) 
);"""

sql4 = """INSERT INTO growth_conditions
  (full_condition_id,full_condition_name,summed_condition_name) 
VALUES 
  (1,'ammonium','ammonium'),
  (2,'histidine','histidine'),
  (3,'lysine','lysine'),
  (6,'extended hypoxia','extended hypoxia'),
  (9,'reaeration day 1','reaerated culture'),
  (12,'reaeration day 2','reaerated culture'),
  (15,'reaeration day 3','exponential'),
  (18,'reaeration day 4','exponential'),
  (21,'butyrate','butyrate'),
  (24,'Butyrate + glucose','butyrate and glucose'),
  (27,'glucose','glucose'),
  (30,'High iron','high iron'),
  (36,'low iron, 1 day','low iron'),
  (37,'low iron 1 week','low iron'),
  (38,'tyloxapol pH7.0','exponential'),
  (40,'tyloxapol pH5.5','acid'),
  (42,'dextrose, exponential','exponential'),
  (44,'Dextrose / Stationary','stationary'),
  (46,'Dextrose / NRP1 dormancy','hypoxia'),
  (48,'Cholesterol + Fatty acids / Exponential','cholesterol'),
  (50,'Cholesterol + Fatty acids / Stationary','cholesterol'),
  (52,'Cholesterol + Fatty acids / NRP1 ','cholesterol')
  ; """

sql5 = """ ALTER TABLE growth_conditions 
ADD FOREIGN KEY (summed_condition_name) REFERENCES summed_growth_conditions(summed_condition_name); 
"""


# Create, index and populate the samples table
sql6 = """CREATE TABLE samples(
    sample_id CHAR(190) NOT NULL PRIMARY KEY,
    dataset_source VARCHAR(190),
    total_reads INT,
    mapped_reads INT,
    instrument VARCHAR(190),
    full_condition_id INT
);"""

sql7 = """ 
INSERT INTO samples
  (sample_id,dataset_source,total_reads,mapped_reads,instrument,full_condition_id) 
VALUES 
  ('ERR2103718','PRJEB65014_3/E-MTAB-6011',9367914,9354741,'Illumina MiSeq',1),
  ('ERR2103722','PRJEB65014_3/E-MTAB-6011',7680627,7652797,'Illumina MiSeq',2),
  ('ERR2103723','PRJEB65014_3/E-MTAB-6011',7154334,7126291,'Illumina MiSeq',3),
  ('SRR1917694','PRJNA278760/GSE67035',16213614,14732714,'Illumina HiSeq 2000',21),
  ('SRR1917695','PRJNA278760/GSE67035',7720838,6862574,'Illumina HiSeq 2000',21),
  ('SRR1917696','PRJNA278760/GSE67035',13765884,12669748,'Illumina HiSeq 2000',21),
  ('SRR1917697','PRJNA278760/GSE67035',25658918,24896850,'Illumina HiSeq 2000',24),
  ('SRR1917698','PRJNA278760/GSE67035',33923728,33002808,'Illumina HiSeq 2000',24),
  ('SRR1917699','PRJNA278760/GSE67035',26142374,25299306,'Illumina HiSeq 2000',24),
  ('SRR1917700','PRJNA278760/GSE67035',63088836,60684742,'Illumina HiSeq 2000',27),
  ('SRR1917701','PRJNA278760/GSE67035',33977392,32648866,'Illumina HiSeq 2000',27),
  ('SRR1917702','PRJNA278760/GSE67035',20196942,19467278,'Illumina HiSeq 2000',27),
  ('SRR1917703','PRJNA278760/GSE67035',40244762,38748652,'Illumina HiSeq 2000',30),
  ('SRR1917704','PRJNA278760/GSE67035',29978232,29023260,'Illumina HiSeq 2000',30),
  ('SRR1917705','PRJNA278760/GSE67035',12226642,11787410,'Illumina HiSeq 2000',30),
  ('SRR1917706','PRJNA278760/GSE67035',4321888,3970194,'Illumina HiSeq 2000',36),
  ('SRR1917707','PRJNA278760/GSE67035',26133582,23731476,'Illumina HiSeq 2000',36),
  ('SRR1917708','PRJNA278760/GSE67035',37686290,31347088,'Illumina HiSeq 2000',36),
  ('SRR1917709','PRJNA278760/GSE67035',43286552,30597890,'Illumina HiSeq 2000',37),
  ('SRR1917710','PRJNA278760/GSE67035',21154872,14993716,'Illumina HiSeq 2000',37),
  ('SRR1917711','PRJNA278760/GSE67035',23028984,19122546,'Illumina HiSeq 2000',37),
  ('SRR1917712','PRJNA278760/GSE67035',30097466,28837844,'Illumina HiSeq 2000',38),
  ('SRR1917713','PRJNA278760/GSE67035',51919310,49722782,'Illumina HiSeq 2000',38),
  ('SRR1917714','PRJNA278760/GSE67035',14284392,13081536,'Illumina HiSeq 2000',40),
  ('SRR1917715','PRJNA278760/GSE67035',14215778,13458292,'Illumina HiSeq 2000',40),
  ('SRR3725585','PRJNA327080/GSE83814',21008310,20938449,'Illumina HiSeq 2000',6),
  ('SRR3725586','PRJNA327080/GSE83814',21415359,21342296,'Illumina HiSeq 2000',6),
  ('SRR3725587','PRJNA327080/GSE83814',18808206,18724155,'Illumina HiSeq 2000',6),
  ('SRR3725588','PRJNA327080/GSE83814',20826329,20771175,'Illumina HiSeq 2000',9),
  ('SRR3725589','PRJNA327080/GSE83814',19531716,19481840,'Illumina HiSeq 2000',9),
  ('SRR3725590','PRJNA327080/GSE83814',21978750,21924251,'Illumina HiSeq 2000',9),
  ('SRR3725591','PRJNA327080/GSE83814',22769048,22713384,'Illumina HiSeq 2000',12),
  ('SRR3725592','PRJNA327080/GSE83814',16588533,16520781,'Illumina HiSeq 2000',12),
  ('SRR3725593','PRJNA327080/GSE83814',20593647,20548622,'Illumina HiSeq 2000',12),
  ('SRR3725594','PRJNA327080/GSE83814',19080715,18981164,'Illumina HiSeq 2000',15),
  ('SRR3725595','PRJNA327080/GSE83814',22792751,22743220,'Illumina HiSeq 2000',15),
  ('SRR3725596','PRJNA327080/GSE83814',21456168,21399192,'Illumina HiSeq 2000',15),
  ('SRR3725597','PRJNA327080/GSE83814',18043065,17990763,'Illumina HiSeq 2000',18),
  ('SRR3725598','PRJNA327080/GSE83814',21192420,21070903,'Illumina HiSeq 2000',18),
  ('SRR3725599','PRJNA327080/GSE83814',23837645,23759073,'Illumina HiSeq 2000',18),
  ('SRR5689224','PRJNA390669/GSE100097',44535192,44464737,'NextSeq 500',42),
  ('SRR5689225','PRJNA390669/GSE100097',43017385,42944835,'NextSeq 500',42),
  ('SRR5689226','PRJNA390669/GSE100097',43380728,43282726,'NextSeq 500',44),
  ('SRR5689227','PRJNA390669/GSE100097',54727622,54595943,'NextSeq 500',44),
  ('SRR5689228','PRJNA390669/GSE100097',53625132,53481181,'NextSeq 500',46),
  ('SRR5689229','PRJNA390669/GSE100097',27184961,27110074,'NextSeq 500',46),
  ('SRR5689230','PRJNA390669/GSE100097',51018804,50928267,'NextSeq 500',48),
  ('SRR5689231','PRJNA390669/GSE100097',46974920,46899380,'NextSeq 500',48),
  ('SRR5689232','PRJNA390669/GSE100097',50593105,50511466,'NextSeq 500',52),
  ('SRR5689233','PRJNA390669/GSE100097',45045262,44954066,'NextSeq 500',50),
  ('SRR5689234','PRJNA390669/GSE100097',55405260,55211551,'NextSeq 500',52),
  ('SRR5689235','PRJNA390669/GSE100097',56890173,56768212,'NextSeq 500',52);
"""

sql8 = """ALTER TABLE samples
ADD FOREIGN KEY (full_condition_id) REFERENCES growth_conditions(full_condition_id); """

# Create, index and populate the modules table
sql9 = """ CREATE TABLE modules(
    module_id VARCHAR(190) PRIMARY KEY,
    module_name VARCHAR(190),
    enrich_utr_qval DEC(15, 12),
    enrich_srna_qval DEC(15, 12),
    mycobrowser_category_enrichment VARCHAR(190) 
);"""

sql10 = """INSERT INTO modules
  (module_id,module_name,enrich_utr_qval,enrich_srna_qval,mycobrowser_category_enrichment)
VALUES 
  ('40E0D0','turquoise',1.000000000,0.000000000,'regulatory proteins, insertion seqs and phages'),
  ('0000FF','blue',0.785402796,0.000017900,'virulence/detoxification/adaptation, regulatory proteins, conserved hypotheticals'),
  ('A52A2A','brown',1.000000000,1.000000000,'information pathways, intermediary metabolism and respiration'),
  ('FFFF00','yellow',0.000114000,1.000000000,'information pathways'),
  ('00FF00','green',0.011802776,1.000000000,''),
  ('FF0000','red',0.000160000,1.000000000,''),
  ('000000','black',0.054381307,1.000000000,''),
  ('BEBEBE','grey',0.982069793,0.251653936,''),
  ('FFC0CB','pink',0.694365630,0.251653936,''),
  ('FF00FF','magenta',0.934809942,1.000000000,'lipid metabolism, PE/PPE'),
  ('A020F0','purple',1.000000000,1.000000000,'virulence/detoxification/adaptation'),
  ('ADFF2F','greenyellow',0.000004450,1.000000000,''),
  ('D2B48C','tan',0.627549614,1.000000000,''),
  ('FA8072','salmon',1.000000000,1.000000000,'insertion seqs and phages'),
  ('00FFFF','cyan',1.000000000,1.000000000,'virulence/detoxification/adaptation, insertion seqs and phages'),
  ('191970','midnightblue',0.054381307,1.000000000,'intermediary metabolism and respiration'),
  ('E0FFFF','lightcyan',1.000000000,1.000000000,'lipid metabolism'),
  ('999999','grey60',1.000000000,1.000000000,''),
  ('90EE90','lightgreen',0.588298931,1.000000000,''),
  ('FFFFE0','lightyellow',0.785402796,1.000000000,''),
  ('4169E1','royalblue',0.182846661,1.000000000,''),
  ('8B0000','darkred',0.073746914,1.000000000,''),
  ('006400','darkgreen',0.148540680,1.000000000,''),
  ('00CED1','darkturquoise',0.694365630,0.080545369,''),
  ('A9A9A9','darkgrey',0.826042946,1.000000000,''),
  ('FF8C00','darkorange',0.017718903,1.000000000,''),
  ('FFA500','orange',0.539771095,1.000000000,''),
  ('87CEEB','skyblue',1.000000000,0.013270057,''),
  ('FFFFFF','white',0.000031800,1.000000000,'lipid metabolism'),
  ('8B4513','saddlebrown',0.147868602,1.000000000,''),
  ('4682B4','steelblue',0.939143659,1.000000000,'lipid metabolism'),
  ('AFEEEE','paleturquoise',1.000000000,1.000000000,''),
  ('EE82EE','violet',0.182846661,1.000000000,''),
  ('556B2F','darkolivegreen',1.000000000,1.000000000,'PE/PPE'),
  ('8B008B','darkmagenta',0.010118660,1.000000000,''),
  ('CD6839','sienna3',0.000952000,1.000000000,''),
  ('9ACD32','yellowgreen',0.021698965,1.000000000,''),
  ('6CA6CD','skyblue3',0.149950027,1.000000000,'cell wall and cell processes'),
  ('FFBBFF','plum1',0.021698965,1.000000000,''),
  ('8B2500','orangered4',1.000000000,1.000000000,''),
  ('8968CD','mediumpurple3',0.785402796,0.124187674,'information pathways'),
  ('E0FFFF1','lightcyan1',0.846280850,1.000000000,''),
  ('CAE1FF','lightsteelblue1',0.037990317,1.000000000,''),
  ('FFFFF0','ivory',1.000000000,0.080545369,''),
  ('FFFAF0','floralwhite',0.785402796,1.000000000,''),
  ('EE7600','darkorange2',0.588298931,1.000000000,''),
  ('8B7D6B','bisque4',1.000000000,1.000000000,''),
  ('8B2323','brown4',0.694365630,1.000000000,''),
  ('483D8B','darkslateblue',1.000000000,1.000000000,''),
  ('EEAEEE','plum2',1.000000000,1.000000000,''),
  ('EED2EE','thistle2',1.000000000,1.000000000,''),
  ('FFE1FF','thistle1',1.000000000,1.000000000,''),
  ('8B4C39','salmon4',1.000000000,1.000000000,''),
  ('CD6889','palevioletred3',0.006241331,1.000000000,''),
  ('EECFA1','navajowhite2',1.000000000,1.000000000,''),
  ('B03060','maroon',0.178976408,1.000000000,'');
"""

# Create, index and populate the module_correlation table
sql11 = """CREATE TABLE module_correlation(
   CONSTRAINT module_correlation_id PRIMARY KEY (module_id, summed_condition_name),
   module_id VARCHAR(190),
   summed_condition_name VARCHAR(190),
   raw_cor DEC(15, 12),
   p_adjusted_cor DEC(15,12)
);"""

sql12 = f""" {mci.values} """


sql13a = """
ALTER TABLE module_correlation
ADD FOREIGN KEY (summed_condition_name) REFERENCES summed_growth_conditions(summed_condition_name); """

sql13b = """ALTER TABLE module_correlation
ADD FOREIGN KEY (module_id) REFERENCES modules(module_id);
"""


# Create, index and populate ELEMENTS TABLE
sql14 = """CREATE TABLE elements(
    element_id VARCHAR(190) PRIMARY KEY,
    element_type ENUM('cds', 'srna', 'utr', 'annotated_ncrna') NOT NULL
);"""

sql15 = f""" INSERT INTO elements
  (element_id,element_type) 
VALUES {em.em_fin}('filler', 'cds');
"""

# Create, index and populate SRNA TABLE
sql16 = """ CREATE TABLE srna(
    srna_element_id VARCHAR(190) PRIMARY KEY,
    srna_name VARCHAR(190),
    seq_start INT NOT NULL,
    seq_end INT NOT NULL,
    strand TEXT NOT NULL,
    tss INT NOT NULL,
    intergenic BOOLEAN,
    gene_element_id VARCHAR(190)
); """

sql17 = f""" {si.values} """

# Create, index and populate UTR TABLE
sql18 = """CREATE TABLE utr(
    utr_element_id VARCHAR(190) PRIMARY KEY,
    seq_start INT NOT NULL,
    seq_end INT NOT NULL,
    strand TEXT NOT NULL,
    tss INT NOT NULL,
    downstream_gene_element_id VARCHAR(190),
    upstream_gene_element_id VARCHAR(190),
    predicted_utr_name VARCHAR(190),
    independent BOOLEAN
);"""

sql19 = f""" {ui.values} """

# Create, index and populate NCRNA TABLE
sql20 = """ CREATE TABLE annotated_ncrna (
  annotated_ncrna_element_id VARCHAR(190) PRIMARY KEY,
  annotated_ncrna_name VARCHAR(190),
  related_srna_name VARCHAR(190)
); """

sql21 = f""" {ni.values} """

# Create, index and populate CDS TABLE
sql22 = """CREATE TABLE cds(
cds_element_id VARCHAR(190) PRIMARY KEY,
cds_name VARCHAR(190),
mycobroswer_functional_category VARCHAR(190),
go_term_mol VARCHAR(190),
go_term_bio VARCHAR(190)
);"""

sql23 = f""" {ci.values} """

sql24a = """ UPDATE cds
SET go_term_bio = NULL
WHERE go_term_bio = 'NA'; """

sql24b = """
UPDATE cds
SET go_term_mol = NULL
WHERE go_term_mol = 'NA'; """

# Create, index and populate GO TERM TABLE
sql25 = """CREATE TABLE go_terms(
  go_term_id VARCHAR(190) PRIMARY KEY,
  go_term_name VARCHAR(190),
  go_term_type VARCHAR(190),
  go_term_def TEXT
);
"""

sql26 = f""" {gti.values} """


# Create, index and populate RELATIONS table

sql27 = """CREATE TABLE relations(
    relation_id INT PRIMARY KEY AUTO_INCREMENT,
    module_id VARCHAR(190),
    element_id VARCHAR(190),
    element_type ENUM('cds', 'srna', 'utr', 'annotated_ncrna') NOT NULL,
    module_match_score DEC(15,12),
    module_colour VARCHAR(190)
);"""

sql28 = f"""{ri.values} """

sql29a = """
UPDATE relations, modules
SET relations.module_id = modules.module_id
WHERE relations.module_colour = modules.module_name;
"""
sql29b = """
ALTER TABLE relations
DROP COLUMN module_colour;
"""



# ADDING FKs to srna, elements, utr, annotated_ncrna, cds and relations tables
sql30a = """ALTER TABLE relations
ADD FOREIGN KEY (module_id) REFERENCES modules(module_id);
"""
sql30b = """ UPDATE elements
set elements.element_id = LTRIM(RTRIM(elements.element_id));
"""
sql30c = """ 
UPDATE relations
set relations.element_id = LTRIM(RTRIM(relations.element_id));

"""
sql30d = """ 
ALTER TABLE relations
ADD FOREIGN KEY (element_id) REFERENCES elements(element_id);

"""
sql30e = """ 
CREATE INDEX element_type_fk
ON elements(element_type);

"""
sql30f = """ 
ALTER TABLE relations
ADD FOREIGN KEY (element_type) REFERENCES elements(element_type);

"""
sql30g = """ 
UPDATE cds
set cds.cds_element_id = LTRIM(RTRIM(cds.cds_element_id));

"""
sql30h = """ 
ALTER TABLE cds
ADD FOREIGN KEY (cds_element_id) REFERENCES elements(element_id);

"""
sql30i = """ 
UPDATE srna
set srna.srna_element_id = LTRIM(RTRIM(srna.srna_element_id));

"""
sql30j = """ 
ALTER TABLE srna
ADD FOREIGN KEY (srna_element_id) REFERENCES elements(element_id);

"""
sql30k = """ 
UPDATE srna
SET srna.gene_element_id = NULL
WHERE srna.gene_element_id = '';

"""
sql30l = """ 
ALTER TABLE srna
ADD FOREIGN KEY (gene_element_id) REFERENCES elements(element_id);

"""
sql30m = """ 
UPDATE utr
set utr.utr_element_id = LTRIM(RTRIM(utr.utr_element_id));

"""
sql30n = """ 
ALTER TABLE utr
ADD FOREIGN KEY (utr_element_id) REFERENCES elements(element_id);

"""
sql30o = """ 
ALTER TABLE utr
ADD FOREIGN KEY (upstream_gene_element_id) REFERENCES elements(element_id);

"""
sql30p = """ 
UPDATE annotated_ncrna
set annotated_ncrna.annotated_ncrna_element_id = LTRIM(RTRIM(annotated_ncrna.annotated_ncrna_element_id));

"""
sql30q = """ 
UPDATE annotated_ncrna
set annotated_ncrna.related_srna_name= LTRIM(RTRIM(annotated_ncrna.related_srna_name));

"""
# ncrna no longer references the related srna name because only 4 appear in the
# srna table, of which can simply be queried to obtain. 
#sql30r = """ 
#ALTER TABLE annotated_ncrna
#ADD FOREIGN KEY (related_srna_name) REFERENCES elements(element_id);
#"""


# test
tester_v = """ """
dropper = """ """

# Drop if exists
sql_drop_tables = str()
for table in tables_list:
    sql_drop_tables = "DROP TABLE IF EXISTS " + table
    cursor.execute(sql_drop_tables)

# Execute cursors

cursor.execute(sql0)
cursor.execute(sql1)    
cursor.execute(sql2)
cursor.execute(sql3)
cursor.execute(sql4)
cursor.execute(sql5)

cursor.execute(sql6)
cursor.execute(sql7)
cursor.execute(sql8)

cursor.execute(sql9)
cursor.execute(sql10)
cursor.execute(sql11)
cursor.execute(sql12)
cursor.execute(sql13a)
cursor.execute(sql13b)

cursor.execute(sql14)
cursor.execute(sql15)
cursor.execute(sql16)
cursor.execute(sql17)
cursor.execute(sql18)
cursor.execute(sql19)
cursor.execute(sql20)
cursor.execute(sql21)
cursor.execute(sql22)
cursor.execute(sql23)

cursor.execute(sql24a)
cursor.execute(sql24b)

cursor.execute(sql25)
cursor.execute(sql26)
cursor.execute(sql27)
cursor.execute(sql28)


cursor.execute(sql29a)
cursor.execute(sql29b)

cursor.execute(sql30a)
cursor.execute(sql30b)
cursor.execute(sql30c)
cursor.execute(sql30d)
cursor.execute(sql30e)
cursor.execute(sql30f)
cursor.execute(sql30g)
cursor.execute(sql30h)
cursor.execute(sql30i)
cursor.execute(sql30j)

cursor.execute(sql30k)
cursor.execute(sql30l)
cursor.execute(sql30m)
cursor.execute(sql30n)
cursor.execute(sql30o)
cursor.execute(sql30p)
cursor.execute(sql30q)








# close and commit
db.commit()
cursor.close()
db.close()
