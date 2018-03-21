from django.shortcuts import render
from django.http import JsonResponse
from channels import Group
from django.conf import settings
from os import path
import csv
import time
from robofork_app.services.can_const import *
from robofork_app.libs import utility, mqtt


def index(request, vehicle_id):
    return render(request, 'robofork_app/mqtt_test.html', {"vehicle_id":vehicle_id})


def route_execute(request, vehicle_id):
    wait_time_sec = 0.025
    sign_offset = 32768

    # ルート情報CSVファイルを開く
    with open(path.join(settings.BASE_DIR, "test_route.csv")) as f:
        reader = csv.reader(f, delimiter="\t")

        # 件数を取得してPreMap送信
        row_count = sum(1 for row in reader)
        f.seek(0)
        mqtt.send(vehicle_id, CAN_ID_MAP_PRE_INFO, utility.to_hex(999) + utility.to_hex(row_count) + "00000000")
        time.sleep(wait_time_sec)
        print("START " + str(row_count))

        # 1件ごと
        for row in reader:
            # 102
            data = (
                    utility.to_hex(int(row[0])) +
                    utility.to_hex(int(float(row[1])) + sign_offset) +
                    utility.to_hex(int(float(row[2])) + sign_offset) +
                    utility.to_hex(int(float(row[4])) + sign_offset))
            # print(data)

            time.sleep(wait_time_sec)
            mqtt.send(vehicle_id, CAN_ID_MAP_INFO_1, data)

            # 103
            data = (
                utility.to_hex(int(row[0])) +
                utility.to_hex(int(row[3]), 2) +
                utility.to_hex(int(row[5]), 2) +
                utility.to_hex(int(float(row[6])) + sign_offset) +
                utility.to_hex(int(float(row[7])) + sign_offset)
            )
            # print(data)

            time.sleep(wait_time_sec)
            mqtt.send(vehicle_id, CAN_ID_MAP_INFO_2, data)
        
        time.sleep(wait_time_sec)
        mqtt.send(vehicle_id, CAN_ID_ACTION, (utility.to_hex(999) + utility.to_hex(1, 2) + utility.to_hex(1, 2) + "00000000"))

    return JsonResponse({'result': True})


def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("mqtt_test").add(message.reply_channel)


def ws_disconnect(message):
    Group("mqtt_test").discard(message.reply_channel)


def ws_message(message):
    Group("mqtt_test").send({
        "text": message.content['text'],
    })
