from django.db import models


class VehicleModel(models.Model):
    name = models.CharField(max_length=100)
    model_no = models.CharField(max_length=100, null=True)
    extra_info_json = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
