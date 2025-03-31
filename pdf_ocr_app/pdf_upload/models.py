from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    total_experience = models.FloatField(blank=True, null=True)  # in years
    gaps = models.TextField(blank=True, null=True)  # gaps in employment
    extracted_text = models.TextField(blank=True, null=True)  # raw text from PDF
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name