from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from robofork_app.libs import mqtt
from robofork_app.services import can_const
from robofork_app.models import Vehicle


@csrf_exempt
def execute(request, location_id):
    # 送信データ作成
    emergency_type = request.POST.get('emergency_type', "0")
    is_cancel = request.POST.get('is_cancel')
    vehicle_id = int(request.POST.get('vehicle_id', 0))

    if is_cancel:
        data = "0000000000000000"
    else:
        data_list = {
            "0": "0100000000000000",
            "1": "0001000000000000",
            "2": "0000010000000000",
        }
        data = data_list.get(emergency_type, "0000000000000000")

    if vehicle_id > 0:
        mqtt.send(vehicle_id, can_const.CAN_ID_SND_EMERGENCY, data)
    else:
        # 存在する全車両に緊急指示を投げる
        vehicles = Vehicle.get_list(location_id=location_id)
        for vehicle in vehicles:
            mqtt.send(vehicle.id, can_const.CAN_ID_SND_EMERGENCY, data)

    return JsonResponse({ "result": True })
