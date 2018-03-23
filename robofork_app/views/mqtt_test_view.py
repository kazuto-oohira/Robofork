from django.shortcuts import render
from django.http import JsonResponse
from channels import Group
from django.conf import settings
import os, csv, json
from robofork_app.services import can_const, route_operation_service
from robofork_app.models import vehicle_operation_plan


def index(request, vehicle_id):
    return render(request, 'robofork_app/mqtt_test.html', {"vehicle_id":vehicle_id})


def route_execute(request, vehicle_id):
    # ルート情報CSVファイルを開く
    with open(os.path.join(settings.BASE_DIR, "robofork_bin/test/test_data/test_route_from_SEIGYO_team.csv")) as f:
        reader = csv.reader(f, delimiter=",")

        # VehicleRouteOperationへテストデータとして登録
        data = []
        for row in reader:
            if int(row[0]) == 0:
                continue

            data_json = {
                "rawIndex": int(row[0]),
                "x": int(row[1]) / 1000,
                "y": int(row[2]) / 1000,
                "task": int(row[3]),
                "afterTask": can_const.ROUTE_TASK_NOTHING,
                "speed": row[4],
                "stop": row[5],
                "angle": row[6],
                "liftHeight": row[7],
            }

            # タスクが荷上げ下げならAfterTaskに登録
            if data_json["task"] == can_const.ROUTE_TASK_LIFTUP \
                    or data_json["task"] == can_const.ROUTE_TASK_LIFTUP_WITH_TURN \
                    or data_json["task"] == can_const.ROUTE_TASK_LIFTDOWN \
                    or data_json["task"] == can_const.ROUTE_TASK_LIFTDOWN_WITH_TURN:
                data_json["afterTask"] = data_json["task"]
                if len(data) > 0:
                    data_json["task"] = data[len(data) -1]["task"]

            # 前回追加したIndexと同じなら今回のはAfterTaskとして登録
            if len(data) > 0 and data_json["rawIndex"] == data[len(data) -1]["rawIndex"]:
                data[len(data) - 1]["afterTask"] = data_json["task"]
            else:
                data.append(data_json)

        # VehicleRouteOperationにテストデータ登録
        plan = vehicle_operation_plan.VehicleOperationPlan()
        plan.vehicle_id = vehicle_id
        plan.name = "テストデータ"
        plan.explain = "制御チームのCSVを登録している"
        plan.location_id = 1
        plan.priority = 9999
        plan.route_operation_json = json.dumps(data)
        plan.save()

        # 送信
        route_operation_service.RouteOperationService.execute_route_operation(plan.id)

        # テストデータ削除
        plan.delete()

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
