from django.urls import path
from .views import *


urlpatterns = [
    path('tribe-form/', tribe_form_view, name='tribe_form'),
    path('<slug>/pdf/', tribe_pdf_view, name='tribe_pdf'),
    path('<name>/<year>/', tribe_detail_view, name='tribe_detail'), 
    path('test/', test_view, name='test'),
     path('download-template/', download_template, name='download_template'),
]



