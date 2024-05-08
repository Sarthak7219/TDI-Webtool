from django.urls import path
from .views import *

urlpatterns = [
    path('<slug1>/<slug2>/', district_view, name='district_view'),
    path('form/',form_view,name='form_detail'),
]