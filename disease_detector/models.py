from django.db import models

# class DiseaseRecord(models.Model):
#     image = models.ImageField(upload_to="disease_images/")
#     disease_name = models.CharField(max_length=255, null=True, blank=True)  # Allow NULL
#     probability = models.CharField(max_length=10, null=True, blank=True)
#     urgency_level = models.CharField(max_length=50, null=True, blank=True)
#     symptoms_analysis = models.TextField(null=True, blank=True)
#     recommended_actions = models.TextField(null=True, blank=True)
#     preventive_care = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

# class DiseaseImage(models.Model):
#     disease_record = models.ForeignKey(DiseaseRecord, related_name="images", on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='disease_images/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)


class DiseaseRecord(models.Model):
    user_id = models.CharField(max_length=255, null=True, blank=False)   
    disease_name = models.CharField(max_length=255, null=True, blank=True)  # Allow NULL
    probability = models.CharField(max_length=10, null=True, blank=True)
    urgency_level = models.CharField(max_length=50, null=True, blank=True)
    symptoms_analysis = models.TextField(null=True, blank=True)
    recommended_actions = models.TextField(null=True, blank=True)
    preventive_care = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.disease_name or "Unnamed Disease"


class DiseaseImage(models.Model):
    disease_record = models.ForeignKey(DiseaseRecord, related_name="images", on_delete=models.CASCADE)
    user_id = models.CharField(max_length=255, null=True, blank=False)
    image = models.ImageField(upload_to='disease_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.disease_record.disease_name} uploaded at {self.uploaded_at}"





