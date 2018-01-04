from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import paho.mqtt.client as mqtt
from channels import Group
from channels.sessions import channel_session


def index(request):
    return render(request, 'robofork_app/mqtt_test.html', None)


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
    client.connect("192.168.1.121", 1883, 60)
    client.publish("Robofork/" + serial_number + "/toR", payload_json)

    return JsonResponse({'result': True})


# @channel_session
def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("can").add(message.reply_channel)


def ws_disconnect(message):
    Group("can").discard(message.reply_channel)


# @channel_session
def ws_message(message):
    Group("can").send({
        "text": message.content['text'],
    })
