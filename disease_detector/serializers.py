from rest_framework import serializers
from .models import DiseaseRecord, DiseaseImage

class DiseaseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseImage
        fields = ['id', 'uploaded_at']

class DiseaseRecordSerializer(serializers.ModelSerializer):
    images = DiseaseImageSerializer(many=True, read_only=True)

    class Meta:
        model = DiseaseRecord
        fields = '__all__'
