from django import forms
from .models import District

class DistrictModelForm(forms.ModelForm):
    class Meta:
        model = District
        fields = [
          
          'name',    
          'year',    
          'st_population',    
          'total_population',    
          'W_BMI',    
          'C_UW' ,   
          'AN_W',    
          'AN_C' ,   
          'AHC_ANC'  ,  
          'AHC_Full_ANC' ,   
          'AHC_PNC',    
          'AHC_HI',    
          'Enrollment',    
          'Equity',    
          'E_DropRate',    
          'S_Sani',    
          'S_CoFu',    
          'S_DrWa',    
          'S_Elec',    
        ]

labels = {
  'name': 'District name',  
  'year': 'Year',    
  'st_population': 'ST Population',    
  'total_population': 'Total Population',    
  'W_BMI': 'Women with BMI below normal score',    
  'C_UW' : 'Children Under weight score',   
  'AN_W': 'Anaemia-Women score',    
  'AN_C' : 'Anaemia- children',
  'AHC_ANC'  : 'Antenatal checkup 1st trimister',
  'AHC_Full_ANC' : 'Full Antenatal care score',   
  'AHC_PNC': 'Post natal care score',    
  'AHC_HI': 'Health Insurance score',    
  'Enrollment': 'ST Enrollment score',    
  'Equity': 'Equity Outcome score',    
  'E_DropRate': 'Drop out score',    
  'S_Sani': 'Sanitation score',    
  'S_CoFu': 'Source of Cooking Fuel score',    
  'S_DrWa': 'Source of Drinking water score',    
  'S_Elec': 'Electricity score', 
}