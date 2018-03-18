import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from robofork_app.models.vehicle_operation_plan import VehicleOperationPlan
from robofork_app.services.route_operation_service import RouteOperationService


@csrf_exempt
def load(request, vehicle_operation_plan_id):
    vehicle_operation_plan = get_object_or_404(VehicleOperationPlan, pk=vehicle_operation_plan_id)

    result_data = {
        "name": vehicle_operation_plan.name,
        "explain": vehicle_operation_plan.explain,
        "priority": vehicle_operation_plan.priority,
        "commands": json.loads(vehicle_operation_plan.route_operation_json),
        "vehicle": vehicle_operation_plan.vehicle.as_json(),
    }

    return JsonResponse(result_data)


@csrf_exempt
def save(request, vehicle_operation_plan_id):
    print(json.dumps(json.loads(request.body), indent=4))

    try:
        vehicle_operation_plan = VehicleOperationPlan.objects.get(pk=vehicle_operation_plan_id)
    except VehicleOperationPlan.DoesNotExist:
        vehicle_operation_plan = VehicleOperationPlan()

    data_json = json.loads(request.body)

    vehicle_operation_plan.id = vehicle_operation_plan_id
    vehicle_operation_plan.route_operation_json = json.dumps(data_json["commands"])
    vehicle_operation_plan.save()

    return JsonResponse({'result': True})


@csrf_exempt
def execute(request, vehicle_operation_plan_id):
    RouteOperationService.execute_route_operation(vehicle_operation_plan_id)
    return JsonResponse({'result': True})