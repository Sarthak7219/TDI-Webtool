from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .models import Profile, Report_Excel
# Register your models here.

class ViewAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    pass

admin.site.register(Profile, ViewAdmin)
admin.site.register(Report_Excel, ViewAdmin)