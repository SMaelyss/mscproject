from django.db import models

# Create your models here.

class AnnotatedNcrna(models.Model):
    annotated_ncrna_element_id = models.CharField(primary_key=True, max_length=190)
    annotated_ncrna_name = models.CharField(max_length=190, blank=True, null=True)
    related_srna_name = models.CharField(max_length=190, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'annotated_ncrna'


class Cds(models.Model):
    cds_element = models.OneToOneField('Elements', models.DO_NOTHING, primary_key=True)
    cds_name = models.CharField(max_length=190, blank=True, null=True)
    mycobroswer_functional_category = models.CharField(max_length=190, blank=True, null=True)
    go_term_mol = models.CharField(max_length=255, blank=True, null=True)
    go_term_bio = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cds'


class Elements(models.Model):
    element_id = models.CharField(primary_key=True, max_length=190)
    element_type = models.CharField(max_length=190)

    class Meta:
        managed = False
        db_table = 'elements'


class GoTerms(models.Model):
    go_term_id = models.CharField(primary_key=True, max_length=190)
    go_term_name = models.CharField(max_length=190, blank=True, null=True)
    go_term_type = models.CharField(max_length=190, blank=True, null=True)
    go_term_def = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'go_terms'


class GrowthConditions(models.Model):
    full_condition_id = models.IntegerField(primary_key=True)
    full_condition_name = models.CharField(max_length=190)
    summed_condition_name = models.ForeignKey('SummedGrowthConditions', models.DO_NOTHING, db_column='summed_condition_name', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'growth_conditions'


class ModuleCorrelation(models.Model):
    module = models.OneToOneField('Modules', models.DO_NOTHING, primary_key=True)
    summed_condition_name = models.ForeignKey('SummedGrowthConditions', models.DO_NOTHING, db_column='summed_condition_name')
    raw_cor = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    p_adjusted_cor = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'module_correlation'
        unique_together = (('module', 'summed_condition_name'),)



class Modules(models.Model):
    module_id = models.CharField(primary_key=True, max_length=190)
    module_name = models.CharField(max_length=190, blank=True, null=True)
    enrich_utr_qval = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    enrich_srna_qval = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    mycobrowser_category_enrichment = models.CharField(max_length=190, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modules'


class Relations(models.Model):
    relation_id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Modules, models.DO_NOTHING, blank=True, null=True)
    element = models.ForeignKey(Elements, models.DO_NOTHING ,blank=True, null=True, related_name='element')
    element_type = models.ForeignKey(Elements, models.DO_NOTHING, db_column='element_type', blank=True, null=True)
    module_match_score = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relations'


class Samples(models.Model):
    sample_id = models.CharField(primary_key=True, max_length=190)
    dataset_source = models.CharField(max_length=190, blank=True, null=True)
    total_reads = models.IntegerField(blank=True, null=True)
    mapped_reads = models.IntegerField(blank=True, null=True)
    instrument = models.CharField(max_length=190, blank=True, null=True)
    full_condition = models.ForeignKey(GrowthConditions, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'samples'


class Srna(models.Model):
    srna_element = models.OneToOneField(Elements, models.DO_NOTHING, primary_key=True, related_name='srna_element')
    srna_name = models.CharField(max_length=190, blank=True, null=True)
    seq_start = models.IntegerField()
    seq_end = models.IntegerField()
    strand = models.TextField()
    tss = models.IntegerField()
    intergenic = models.IntegerField(blank=True, null=True)
    gene_element = models.ForeignKey(Elements, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'srna'


class SummedGrowthConditions(models.Model):
    summed_condition_id = models.AutoField(primary_key=True)
    summed_condition_name = models.CharField(max_length=190)

    class Meta:
        managed = False
        db_table = 'summed_growth_conditions'


class Utr(models.Model):
    utr_element = models.OneToOneField(Elements, models.DO_NOTHING, primary_key=True, related_name='utr_element')
    seq_start = models.IntegerField()
    seq_end = models.IntegerField()
    strand = models.TextField()
    tss = models.IntegerField()
    downstream_gene_element_id = models.CharField(max_length=190, blank=True, null=True)
    upstream_gene_element = models.ForeignKey(Elements, models.DO_NOTHING, blank=True, null=True)
    predicted_utr_name = models.CharField(max_length=190, blank=True, null=True)
    independent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'utr'

