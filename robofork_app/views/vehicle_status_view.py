from django.shortcuts import render, redirect, get_object_or_404
from robofork_app.models.vehicle import Vehicle, VehicleForm


def index(request, location_id):
    vehicles = Vehicle.objects.all()
    return render(request, 'robofork_app/vehicle_status/index.html', {'vehicles': vehicles})
