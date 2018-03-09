from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from channels import Group
from django.conf import settings
from os import path
import csv
import time
from robofork_app.libs import utility, mqtt


def index(request):
    return render(request, 'robofork_app/mqtt_test.html', None)


def route_execute(request):
    wait_time_sec = 0.025
    sign_offset = 32768

    # ルート情報CSVファイルを開く
    with open(path.join(settings.BASE_DIR, "test_route.csv")) as f:
        reader = csv.reader(f, delimiter="\t")

        # 件数を取得してPreMap送信
        row_count = sum(1 for row in reader)
        f.seek(0)
        mqtt.send("1", "101", utility.to_can_data(utility.to_hex(999) + utility.to_hex(row_count) + "00000000"))
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
            mqtt.send("1", "102", data)

            # 103
            data = utility.to_can_data(
                utility.to_hex(index) +
                utility.to_hex(int(row[3]), 2) +
                utility.to_hex(int(row[5]), 2) +
                utility.to_hex(int(float(row[6])) + sign_offset) +
                utility.to_hex(int(float(row[7])) + sign_offset)
            )
            print(data)

            time.sleep(wait_time_sec)
            mqtt.send("1", "103", data)

            index += 1
        
        time.sleep(wait_time_sec)
        mqtt.send("1", '104', utility.to_can_data(utility.to_hex(999) + utility.to_hex(1, 2) + utility.to_hex(1, 2) + "00000000"))

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
