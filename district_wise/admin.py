from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from django.contrib.auth import get_user_model
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

User = get_user_model()
# Register your models here.

class DistrictResource(resources.ModelResource):
    user = Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'phone_number'))    

    class Meta:
        model = District
        import_id_fields = ('id',)  # Assuming 'id' is the primary key

class DistrictAdmin(ImportExportModelAdmin):
    resource_class = DistrictResource

admin.site.register(District, DistrictAdmin)




