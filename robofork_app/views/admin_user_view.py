from django.shortcuts import render, redirect, get_object_or_404
from robofork_app.models.vehicle import Vehicle, VehicleForm


def index(request):
    return render(request, 'robofork_app/admin_user/index.html', {'users': None})


def new(request):
    return render(request, 'robofork_app/admin_location/detail.html', {'form': None})


def detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    return render(request, 'robofork_app/admin_vehicle/detail.html', {'form': VehicleForm(instance=vehicle)})


def save(request, vehicle_id=None):
    if vehicle_id:
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    else:
        vehicle = Vehicle()

    vehicle_form = VehicleForm(request.POST, instance=vehicle)
    if vehicle_form.is_valid():
        vehicle_form.save()
        return redirect('vehicle_index')
    else:
        return render(request, 'robofork_app/admin_vehicle/detail.html', {'form': vehicle_form})
