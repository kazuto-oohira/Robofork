from django.shortcuts import render, get_object_or_404
from robofork_app.models import Vehicle, Location, VehicleOperationPlan
# from robofork_app.models.vehicle_operation_plan import  VehicleOperationPlan


def index(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    vehicles = Vehicle.get_list(location_id=location_id)
    return render(request, 'robofork_app/sp/index.html', {
        'location': location,
        'vehicles': vehicles,
    })

def control(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    return render(request, 'robofork_app/sp/control.html', {
        'vehicle': vehicle,
    })

def status(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    return render(request, 'robofork_app/sp/status.html', {
        'vehicle': vehicle,
    })


def operation_plan(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    operation_plan_list = VehicleOperationPlan.objects.filter(vehicle_id=vehicle_id)

    return render(request, 'robofork_app/sp/operation_plan.html', {
        'vehicle': vehicle,
        'operation_plan_list': operation_plan_list
    })


