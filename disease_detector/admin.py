from django.contrib import admin
from .models import DiseaseRecord

@admin.register(DiseaseRecord)
class DiseaseRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'disease_name', 'probability', 'created_at')
