from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.AnnotatedNcrna)
admin.site.register(models.Cds)
admin.site.register(models.GoTerms)
admin.site.register(models.Elements)
admin.site.register(models.GrowthConditions)
admin.site.register(models.Modules)
admin.site.register(models.ModuleCorrelation)
admin.site.register(models.Samples)
admin.site.register(models.Relations)
admin.site.register(models.Srna)
admin.site.register(models.SummedGrowthConditions)
admin.site.register(models.Utr)






