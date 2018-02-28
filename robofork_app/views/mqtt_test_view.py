from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import paho.mqtt.client as mqtt
from channels import Group
from django.conf import settings
from os import path
import csv


# 定数
MQTT_SERVER = '192.168.13.101'


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
        'data': to_can_data(can_data)
    }
    payload_json = json.dumps(payload_data)
    
    print(payload_json)

    # MQTT送信
    client = mqtt.Client()
    client.connect(MQTT_SERVER, 1883, 60)
    client.publish("Robofork/" + serial_number + "/toR", payload_json)
    client.disconnect()

    return JsonResponse({'result': True})


def route_execute(request):
    # MQTT
    client = mqtt.Client()
    client.connect(MQTT_SERVER, 1883, 60)

    # ルート情報CSVファイルを開く
    with open(path.join(settings.BASE_DIR, "test_route.csv")) as f:
        reader = csv.reader(f, delimiter="\t")

        # 件数を取得してPreMap送信
        row_count = sum(1 for row in reader)
        f.seek(0)
        client.publish("Robofork/1/toR", json.dumps({
            'serial_number': '1',
            'id': '101',
            'data': to_can_data(to_hex(999) + to_hex(row_count) + "00000000")
        }))
        print("START " + str(row_count))

        # 1件ごと
        index = 1
        for row in reader:
            # 102
            data = to_can_data(
                to_hex(index) +
                to_hex(int(float(row[1]) * 1000) + 32768) +
                to_hex(int(float(row[2]) * 1000) + 32768) +
                to_hex(int(float(row[4])) + 32768)
            )
            print(data)
            client.connect(MQTT_SERVER, 1883, 60)
            client.publish("Robofork/1/toR", json.dumps({
                'serial_number': '1',
                'id': '102',
                'data': data
            }))

            # 103
            data = to_can_data(
                to_hex(index) +
                to_hex_2(int(row[3])) +
                to_hex_2(int(row[5])) +
                to_hex(int(float(row[6]) * 1000) + 32768) +
                to_hex(int(float(row[7]) * 1000) + 32768)
            )
            print(data)
            client.connect(MQTT_SERVER, 1883, 60)
            client.publish("Robofork/1/toR", json.dumps({
                'serial_number': '1',
                'id': '103',
                'data': data
            }))

            index += 1

        client.connect(MQTT_SERVER, 1883, 60)
        client.publish("Robofork/1/toR", json.dumps({
            'serial_number': '1',
            'id': '104',
            'data': to_can_data(to_hex(999) + to_hex_2(1) + to_hex_2(1) + "00000000")
        }))
        print("END")

    client.disconnect()
    return JsonResponse({'result': True})


def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("can").add(message.reply_channel)


def ws_disconnect(message):
    Group("can").discard(message.reply_channel)


def ws_message(message):
    Group("can").send({
        "text": message.content['text'],
    })


def to_hex(value):
    return hex(value).split('x')[-1].zfill(4)


def to_hex_2(value):
    return hex(value).split('x')[-1].zfill(2)


def to_can_data(value):
    return [(i + j) for (i, j) in zip(value[::2], value[1::2])]
