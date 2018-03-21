from django.shortcuts import render, redirect, get_object_or_404
from robofork_app.models.vehicle import Vehicle, VehicleForm, Location


def index(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    vehicles = Vehicle.get_list(location_id=location_id)
    return render(request, 'robofork_app/sp/index.html', {
        'location': location,
        'vehicles': vehicles,
    })
