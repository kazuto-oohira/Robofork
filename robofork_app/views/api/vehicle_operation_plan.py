from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from robofork_app.models.vehicle_operation_plan import VehicleOperationPlan
from robofork_app.services.route_operation_service import RouteOperationService


@csrf_exempt
def config(request, vehicle_operation_plan_id=1):
    return JsonResponse(
        {
            "config": {
                "imageUrl": "/api/file/1",
                "imageWidth": 502,
                "imageHeight": 394,
                "scaleX": "13.210526316",
                "scaleY": "10.368421053",
                "offsetX": "-2.5",
                "offsetY": "0",
                "startX": "-7.9",
                "startY": "-1.2",
                "startDirection": 1,
            }
        }
    )


@csrf_exempt
def load(request, vehicle_operation_plan_id=1):
    vehicle_operation_plan = get_object_or_404(VehicleOperationPlan, pk=vehicle_operation_plan_id)

    result_data = {
        "name": 'R05-1段目からR06-2段目へ',
        "commands": json.loads(vehicle_operation_plan.route_operation_json)
    }

    return JsonResponse(result_data)


@csrf_exempt
def save(request, vehicle_operation_plan_id=1):
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
def execute(request, vehicle_operation_plan_id=1):
    RouteOperationService.execute_route_operation(vehicle_operation_plan_id)
    return JsonResponse({'result': True})