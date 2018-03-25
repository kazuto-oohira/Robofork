import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from channels import Group
from robofork_app.models.vehicle import Vehicle

@csrf_exempt
def load(request, location_id=1):
    vehicles = Vehicle.get_list(location_id=location_id)

    result = {
        "vehicles": []
    }

    for vehicle in vehicles:
        vehicle_data = {
            "id": vehicle.id,
            "name": vehicle.name,
            "no": vehicle.vehicle_no,
            "vehicle_model_name": vehicle.vehicle_model.name,
            "vehicle_status": {
                "vehicle_operation_plan_id": 0,
                "status_code": 0,
                "status_name": "-",
            },
            "vehicle_positions": [
                {
                    "datetime": "2018-03-20T09:00:00+09:00",
                    "x": "-7.90",
                    "y": "-1.20",
                    "task": 255,
                    "speed": 0,
                    "angle": 0
                }
            ]
        }
        result["vehicles"].append(vehicle_data)

    return JsonResponse(result)


def ws_add(message, location_id=1):
    message.reply_channel.send({"accept": True})
    Group("operation_status").add(message.reply_channel)


def ws_disconnect(message, location_id=1):
    Group("operation_status").discard(message.reply_channel)


def ws_message(message, location_id=1):
    Group("operation_status").send({
        "text": message.content['text'],
    })
