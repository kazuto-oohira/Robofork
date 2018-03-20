from django.db import models
from .location import Location
from .vehicle import Vehicle


class VehicleOperationPlan(models.Model):
    name = models.CharField(max_length=100)
    explain = models.TextField(null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    priority = models.IntegerField(default=0)
    route_operation_json = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @classmethod
    def next_id(cls):
        records = cls.objects.all().order_by("-id")
        if not records:
            return 1
        else:
            return records[0].id + 1

    @classmethod
    def get_list(cls, *, location_id):
        return cls.objects.filter(location_id=location_id).order_by("id")