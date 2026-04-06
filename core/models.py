from django.db import models

class Diagnosis(models.Model):
    image = models.ImageField(upload_to='uploads/')
    plant = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plant} - {self.condition}"