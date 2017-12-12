from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from robofork_app.models import Vehicle


def index(request):
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles
    }
    return render(request, 'robofork_app/vehicle_view/index.html', context)


def new(request):
    return render(request, 'robofork_app/vehicle_view/detail.html', None)


def detail(request, vehicle_id):
    # vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    vehicle = Vehicle.objects.filter(id=vehicle_id)
    if vehicle.count() <= 0:
        return HttpResponseNotFound()

    context = {
        'vehicle': vehicle.first()
    }
    return render(request, 'robofork_app/vehicle_view/detail.html', context)


def save(request):
    vehicle = Vehicle()
    vehicle.name = request.POST['vehicle[name]']
    vehicle.vehicle_no = request.POST['vehicle[vehicle_no]']
    vehicle.save()

    return redirect('vehicle_index')
