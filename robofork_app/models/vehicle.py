import json
from django.db import models
from django.forms import ModelForm
from .vehicle_model import VehicleModel


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    vehicle_no = models.CharField(max_length=100, null=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, null=True)
    extra_info_json = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def as_json(self):
        return {
            "name": self.name,
            "vehicle_no": self.vehicle_no,
            "vehicle_model": self.vehicle_model.as_json() if self.vehicle_model else None,
            "extra_info_json": json.loads(self.extra_info_json or "{}")
        }


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['created_at', 'updated_at']
        # localized_fields = '__all__'

