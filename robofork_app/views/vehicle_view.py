from django.shortcuts import render, redirect
from robofork_app.models import Vehicle


def index(request):
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles
    }
    return render(request, 'robofork_app/vehicle_view/index.html', context)


def new(request):
    return render(request, 'robofork_app/vehicle_view/detail.html', None)


def save(request):
    vehicle = Vehicle()
    vehicle.name = request.POST['vehicle[name]']
    vehicle.vehicle_no = request.POST['vehicle[vehicle_no]']
    vehicle.save()

    return redirect('vehicle_index')
