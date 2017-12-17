from django.db import models
from django.forms import ModelForm


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    vehicle_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['created_at', 'updated_at']
        # localized_fields = '__all__'

