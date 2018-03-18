from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    map_image = models.BinaryField(null=True)
    map_information_json = models.TextField(null=True)
    plc_data_json = models.TextField(null=True)
    fire_doors_json = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
