from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import paho.mqtt.client as mqtt
from channels import Group
from django.conf import settings
from os import path
import csv
import time
from robofork_app.libs import utility


# 定数
MQTT_SERVER = settings.MQTT_SERVER['IP']
MQTT_PORT = settings.MQTT_SERVER['PORT']


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
        'data':  utility.to_can_data(can_data)
    }
    payload_json = json.dumps(payload_data)
    
    print(payload_json)

    # MQTT送信
    client = mqtt.Client()
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    client.publish("Robofork/" + serial_number + "/toR", payload_json)
    client.disconnect()

    return JsonResponse({'result': True})


def route_execute(request):
    wait_time_sec = 0.025
    sign_offset = 32768

    # MQTT
    client = mqtt.Client()
    client.connect(MQTT_SERVER, MQTT_PORT, 60)

    # ルート情報CSVファイルを開く
    with open(path.join(settings.BASE_DIR, "test_route.csv")) as f:
        reader = csv.reader(f, delimiter="\t")

        # 件数を取得してPreMap送信
        row_count = sum(1 for row in reader)
        f.seek(0)
        client.publish("Robofork/1/toR", json.dumps({
            'serial_number': '1',
            'id': '101',
            'data': utility.to_can_data(utility.to_hex(999) + utility.to_hex(row_count) + "00000000")
        }))
        time.sleep(wait_time_sec)
        print("START " + str(row_count))

        # 1件ごと
        index = 1
        for row in reader:
            # 102
            data = utility.to_can_data(
                utility.to_hex(index) +
                utility.to_hex(int(float(row[1])) + sign_offset) +
                utility.to_hex(int(float(row[2])) + sign_offset) +
                utility.to_hex(int(float(row[4])) + sign_offset)
            )
            print(data)

            time.sleep(wait_time_sec)
            client.connect(MQTT_SERVER, MQTT_PORT, 60)
            client.publish("Robofork/1/toR", json.dumps({
                'serial_number': '1',
                'id': '102',
                'data': data
            }))

            # 103
            data = utility.to_can_data(
                utility.to_hex(index) +
                utility.to_hex_2(int(row[3])) +
                utility.to_hex_2(int(row[5])) +
                utility.to_hex(int(float(row[6])) + sign_offset) +
                utility.to_hex(int(float(row[7])) + sign_offset)
            )
            print(data)

            time.sleep(wait_time_sec)
            client.connect(MQTT_SERVER, MQTT_PORT, 60)
            client.publish("Robofork/1/toR", json.dumps({
                'serial_number': '1',
                'id': '103',
                'data': data
            }))

            index += 1
        
        time.sleep(wait_time_sec)
        client.connect(MQTT_SERVER, MQTT_PORT, 60)
        client.publish("Robofork/1/toR", json.dumps({
            'serial_number': '1',
            'id': '104',
            'data': utility.to_can_data(utility.to_hex(999) + utility.to_hex_2(1) + utility.to_hex_2(1) + "00000000")
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
