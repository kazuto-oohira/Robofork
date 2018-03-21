import time, csv, json
from .can_const import *
from robofork_app.libs import utility, mqtt
from robofork_app.models.vehicle_operation_plan import VehicleOperationPlan


class RouteOperationService:

    CAN_SEND_WAIT_TIME_SEC = 0.025

    @classmethod
    def execute_route_operation(cls, vehicle_operation_plan_id=1):

        # ルート情報を取得する（取得不可なら落ちる）
        vehicle_operation_plan = VehicleOperationPlan.objects.get(pk=vehicle_operation_plan_id)
        route_operation_json = json.loads(vehicle_operation_plan.route_operation_json)

        if len(route_operation_json) == 0:
            return

        # なにもしないタスク(255)は送らない
        edit_route_operation = []
        for row in route_operation_json:
            if row.get("task", 255) != 255:
                edit_route_operation.append(row)

        # 件数を取得してPreMap送信
        mqtt.send(vehicle_operation_plan.vehicle_id, CAN_ID_MAP_PRE_INFO,
                  utility.to_hex(vehicle_operation_plan_id) + utility.to_hex(len(edit_route_operation)) + "00000000")
        time.sleep(cls.CAN_SEND_WAIT_TIME_SEC)

        for i in range(2):  # どうにもECUがCANを取りこぼすので2回連続で送る
            index = 1
            for row in edit_route_operation:

                # 初期値設定＆Populate
                data = {
                    "index": index,
                    "x": int(float(row.get("x", 0)) * 1000),
                    "y": int(float(row.get("y", 0)) * 1000),
                    "speed": int(1000),
                    # "speed": int(row.get("speed", 0)),    # なぜか速度がこないけどまぁいいや
                    "task": int(row.get("task", 255)),
                    "after_task": int(row.get("afterTask", 255)),
                    "flag_stop": int(row.get("stop", 0)),
                    "angle": int(row.get("angle", 0)),
                    "height_lift": int(row.get("liftHeight", 0))
                }

                # ===================================
                # AfterTaskを1行で送信するバージョン
                # ===================================
                # AfterTaskが定義されていればflag_stopをONにして、TaskをAfterTaskで置き換える
                if data["after_task"] != 255:
                    data["task"] = data["after_task"]
                    data["flag_stop"] = 1

                # 最後の行なら必ずflag_stopをONにする
                if index == len(edit_route_operation):
                    data["flag_stop"] = 1

                # 送信
                cls.__send_route_data(vehicle_operation_plan.vehicle_id, data)

                # ===================================
                # AfterTaskを2行にして送信するバージョン
                # ===================================
                """
                # AfterTaskが定義されていれば、flag_stopをONに
                if data["after_task"] != 255:
                    data["flag_stop"] = 1

                # 送信
                cls.__send_route_data(vehicle_operation_plan.vehicle_id, data)

                # AfterTaskが定義されていれば、AfterTaskをTaskに置き換えて再送信
                if data["after_task"] != 255:
                    data["flag_stop"] = 0
                    data["task"] = data["after_task"]
                    cls.__send_route_data(vehicle_operation_plan.vehicle_id, data)
                """

                index += 1

        # 実行開始
        time.sleep(cls.CAN_SEND_WAIT_TIME_SEC)
        mqtt.send(vehicle_operation_plan.vehicle_id, CAN_ID_ACTION,
                  utility.to_hex(999) + utility.to_hex(1, 2) + utility.to_hex(1, 2) + "00000000")

    @classmethod
    def __send_route_data(cls, vehicle_id, populated_data):
        # 位置
        can_data = (
            utility.to_hex(populated_data["index"]) +
            utility.to_hex(utility.to_can_signed(populated_data["x"])) +
            utility.to_hex(utility.to_can_signed(populated_data["y"])) +
            utility.to_hex(utility.to_can_signed(populated_data["speed"]))
        )
        time.sleep(cls.CAN_SEND_WAIT_TIME_SEC)
        mqtt.send(vehicle_id, CAN_ID_MAP_INFO_1, can_data)

        # タスク
        can_data = (
            utility.to_hex(populated_data["index"]) +
            utility.to_hex(populated_data["task"], 2) +
            utility.to_hex(populated_data["flag_stop"], 2) +
            utility.to_hex(utility.to_can_signed(populated_data["angle"])) +
            utility.to_hex(utility.to_can_signed(populated_data["height_lift"]))
        )
        time.sleep(cls.CAN_SEND_WAIT_TIME_SEC)
        mqtt.send(vehicle_id, CAN_ID_MAP_INFO_2, can_data)

        print("Route GO: " + str(populated_data))
