from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from import_export import resources, fields
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from .models import  Tribe,Tribe_Image
from accounts.models import Profile
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
class TribeAdminForm(forms.ModelForm):
    class Meta:
        model = Tribe
        fields = '__all__' 
        widgets = {
            'village_details': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class TribeResource(resources.ModelResource):
    user = Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'phone_number'))
    class Meta:
        model = Tribe
        import_id_fields = ('id',)  # Assuming 'id' is the primary key  

class TribeImageResource(resources.ModelResource):
    tribe = Field(column_name='tribe_id', attribute='tribe', widget=ForeignKeyWidget(Tribe, 'id'))
    class Meta:
        model = Tribe_Image
        import_id_fields = ('id',)  # Assuming 'id' is the primary key

class TribeAdmin(ImportExportModelAdmin):
    form = TribeAdminForm
    resource_class = TribeResource

class TribeImageAdmin(ImportExportModelAdmin):
    resource_class = TribeImageResource


admin.site.register(Tribe, TribeAdmin)
admin.site.register(Tribe_Image, TribeImageAdmin)



