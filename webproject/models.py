# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AnnotatedNcrna(models.Model):
    annotated_ncrna_element_id = models.CharField(primary_key=True, max_length=190)
    annotated_ncrna_name = models.CharField(max_length=190, blank=True, null=True)
    related_srna_name = models.CharField(max_length=190, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'annotated_ncrna'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cds(models.Model):
    cds_element = models.OneToOneField('Elements', models.DO_NOTHING, primary_key=True)
    cds_name = models.CharField(max_length=190, blank=True, null=True)
    mycobroswer_functional_category = models.CharField(max_length=190, blank=True, null=True)
    go_term_mol = models.CharField(max_length=255, blank=True, null=True)
    go_term_bio = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cds'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
    element = models.ForeignKey(Elements, models.DO_NOTHING, blank=True, null=True)
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
    srna_element = models.OneToOneField(Elements, models.DO_NOTHING, primary_key=True)
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
    utr_element = models.OneToOneField(Elements, models.DO_NOTHING, primary_key=True)
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
