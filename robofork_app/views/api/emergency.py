from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from robofork_app.libs import mqtt
from robofork_app.services import can_const
from robofork_app.models import Vehicle

from django.shortcuts import get_object_or_404
import django.urls as urls
import json

from robofork_app.models.location import Location


@csrf_exempt
def execute(request, location_id):
    # 送信データ作成
    emergency_type = request.POST.get('emergency_type', "0")



    # 存在する全車両に緊急指示を投げる
    vehicles = Vehicle.get_list(location_id=location_id)
    for vehicle in vehicles:
        mqtt.send(vehicle.id, can_const.CAN_ID_EMERGENCY, None)

    return JsonResponse({ "result": True })


def __execute_or_cancel(request, location_id, is_execute=1):
    pass