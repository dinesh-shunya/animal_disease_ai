from django.contrib import admin 
from django.urls import path  
from .views import *

urlpatterns=[
    path('find_disease/',DiseaseDetector.as_view(),name='find_disease'),
    path('find_animal/',GetAnimal.as_view(),name='find_animal'),
]
