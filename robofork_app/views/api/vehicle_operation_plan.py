from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from robofork_app.libs import mqtt
from robofork_app.models.vehicle_operation_plan import VehicleOperationPlan


@csrf_exempt
def config(request, vehicle_operation_plan_id=1):
    return JsonResponse(
        {
            "config": {
                "imageUrl": "/static/robofork_app/img/test/map1.png",
                "imageWidth": 502,
                "imageHeight": 394,
                "scaleX": "13.210526316",
                "scaleY": "10.368421053",
                "offsetX": "-2.5",
                "offsetY": "0",
                "startX": "-9.56",
                "startY": "-0.26"
            }
        }
    )


@csrf_exempt
def save(request, vehicle_operation_plan_id=1):
    print(json.dumps(json.loads(request.body), indent=4))

    try:
        vehicle_operation_plan = VehicleOperationPlan.objects.get(pk=vehicle_operation_plan_id)
    except VehicleOperationPlan.DoesNotExist:
        vehicle_operation_plan = VehicleOperationPlan()

    vehicle_operation_plan.id = vehicle_operation_plan_id
    vehicle_operation_plan.route_operation_json = json.dumps(json.loads(request.body))
    vehicle_operation_plan.save()

    """
    vehicle_form = VehicleForm(request.POST, instance=vehicle_operation_plan)
    if vehicle_form.is_valid():
        vehicle_form.save()
        return redirect('vehicle_index')
    else:
        return render(request, 'robofork_app/vehicle_view/detail.html', {'form': vehicle_form})
    """

    return JsonResponse({'result': True})


@csrf_exempt
def load(request, vehicle_operation_plan_id=1):
    vehicle_operation_plan = get_object_or_404(VehicleOperationPlan, pk=vehicle_operation_plan_id)
    print(vehicle_operation_plan.route_operation_json)

    data = json.loads(vehicle_operation_plan.route_operation_json)
    return JsonResponse(data)
