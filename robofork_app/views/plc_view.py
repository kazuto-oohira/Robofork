from django.http import JsonResponse
from robofork_app.models import Vehicle
from robofork_app.libs import mqtt
from robofork_app.services import can_const


def execute(request, plc_id):
    # 存在する全車両に緊急指示を投げる
    vehicles = Vehicle.get_list(location_id=1)  # ひとまず1固定
    for vehicle in vehicles:
        mqtt.send(vehicle.id, can_const.CAN_ID_SND_EMERGENCY, "0100000000000000")

    return JsonResponse({"result": True, "id": plc_id})
