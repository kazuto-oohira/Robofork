from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import paho.mqtt.client as mqtt


@csrf_exempt
def send(request):
    # 送信データ編集
    serial_number = "1"
    can_id = request.POST['can_id']
    can_data = request.POST['can_data']
    payload_data = {
        'serial_number': serial_number,
        'id': can_id,
        # 'data': can_data,
        'data': [(i + j) for (i, j) in zip(can_data[::2], can_data[1::2])],
    }
    payload_json = json.dumps(payload_data)

    # MQTT送信
    client = mqtt.Client()
    client.connect("192.168.100.29", 1883, 60)
    client.publish("Robofork/" + serial_number + "/toR", payload_json)

    return JsonResponse({'result': True})


@csrf_exempt
def receive(request):
    payload = json.loads(request.POST['payload'])

    print(payload["serial_number"] + ":" + payload["id"] + ":" + ' '.join(payload["data"]))

    return JsonResponse({'result': True})
