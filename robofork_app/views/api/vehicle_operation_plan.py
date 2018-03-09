from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from robofork_app.libs import mqtt
from robofork_app.models.vehicle_operation_plan import VehicleOperationPlan


@csrf_exempt
def save(request, vehicle_operation_plan_id=1):
    print(json.dumps(json.loads(request.body), indent=4))

    if vehicle_operation_plan_id:
        vehicle_operation_plan = get_object_or_404(VehicleOperationPlan, pk=vehicle_operation_plan_id)
    else:
        # しばらく入らんやろ
        vehicle_operation_plan = VehicleOperationPlan()

    vehicle_operation_plan.route_operation_json = request.body
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
