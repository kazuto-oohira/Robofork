from django.shortcuts import render, redirect
from robofork_app.models import Vehicle, VehicleOperationPlan


def index(request, location_id):
    # 車両取得
    vehicles = Vehicle.get_list(location_id=location_id)

    # 運行計画
    operation_plans = VehicleOperationPlan.get_list(location_id=location_id)

    return render(request, 'robofork_app/home/index.html', {
        'vehicles': vehicles,
        'operation_plans': operation_plans,
    })
