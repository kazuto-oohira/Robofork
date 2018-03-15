import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from channels import Group
from django.shortcuts import get_object_or_404
from robofork_app.libs import mqtt
from robofork_app.models.vehicle_operation_plan import VehicleOperationPlan


@csrf_exempt
def load(request):
    return JsonResponse(
        {
            "vehicles": [
                {
                    "id": 1,
                    "name": "滋賀#1",
                    "no": "SG-FX15-1",
                    "vehicle_model_name": "FX15",
                    "vehicle_status": {
                        "vehicle_operation_plan_id": 1,
                        "status_code": 0,
                        "status_name": "-"
                    },
                    "vehicle_positions": [
                        {
                            "datetime": "2018-03-20T09:00:00+09:00",
                            "x": "-9.57",
                            "y": "-4.50",
                            "task": 0,
                            "speed": 1000,
                            "angle": 0
                        },
                        {
                            "datetime": "2018-03-20T09:00:01+09:00",
                            "x": "-9.67",
                            "y": "-4.80",
                            "task": 0,
                            "speed": 1000,
                            "angle": 0
                        }
                    ]
                }
            ]
        }
    )


def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("operation_status").add(message.reply_channel)


def ws_disconnect(message):
    Group("operation_status").discard(message.reply_channel)


def ws_message(message):
    print(message.content)

    Group("operation_status").send({
        "text": message.content['text'],
    })
