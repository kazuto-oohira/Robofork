import time, csv, json
from robofork_app.libs import utility, mqtt
from robofork_app.models.vehicle_operation_plan import VehicleOperationPlan


class RouteOperationService:

    CAN_SEND_WAIT_TIME_SEC = 0.035

    @classmethod
    def execute_route_operation(cls, vehicle_operation_plan_id=1):

        # ルート情報を取得する（取得不可なら落ちる）
        vehicle_operation_plan = VehicleOperationPlan.objects.get(pk=vehicle_operation_plan_id)
        route_operation_json = json.loads(vehicle_operation_plan.route_operation_json)
        vehicle_id = "1"

        # 件数を取得してPreMap送信
        if len(route_operation_json) == 0:
            return

        # 101(件数)
        mqtt.send(vehicle_id, "101",
                  utility.to_hex(vehicle_operation_plan_id) + utility.to_hex(len(route_operation_json)) + "00000000")
        time.sleep(cls.CAN_SEND_WAIT_TIME_SEC)

        for index, row in enumerate(route_operation_json):
            # 初期値設定＆Populate
            data = {
                "index": index,
                "x": int(float(row.get("x", 0)) * 1000),
                "y": int(float(row.get("y", 0)) * 1000),
                "speed": int(row.get("speed", 0)),
                "task": int(row.get("task", 255)),
                "after_task": int(row.get("afterTask", 255)),
                "flag_stop": 0,
                "angle": int(row.get("angle", 0)),
                "height_lift": int(row.get("liftHeight", 0))
            }

            # TODO: AfterTaskのところ仕様これでいいか確認？
            # AfterTaskが定義されていれば、flag_stopをONに
            if data["after_task"] != 255:
                data["flag_stop"] = 1

            # 送信
            cls.__send_route_data(vehicle_id, data)

            # AfterTaskが定義されていれば、AfterTaskをTaskに置き換えて再送信
            if data["after_task"] != 255:
                data["flag_stop"] = 0
                data["task"] = data["after_task"]
                cls.__send_route_data(vehicle_id, data)

        # 104
        time.sleep(cls.CAN_SEND_WAIT_TIME_SEC)
        mqtt.send(vehicle_id, "104",
                  utility.to_hex(999) + utility.to_hex(1, 2) + utility.to_hex(1, 2) + "00000000")

    @classmethod
    def __send_route_data(cls, vehicle_id, populated_data):
        can_data = (
            utility.to_hex(populated_data["index"]) +
            utility.to_hex(utility.to_can_unsigned_to_signed(populated_data["x"])) +
            utility.to_hex(utility.to_can_unsigned_to_signed(populated_data["y"])) +
            utility.to_hex(utility.to_can_unsigned_to_signed(populated_data["speed"]))
        )
        time.sleep(cls.CAN_SEND_WAIT_TIME_SEC)
        mqtt.send(vehicle_id, "102", can_data)

        # 103
        can_data = (
            utility.to_hex(populated_data["index"]) +
            utility.to_hex(populated_data["task"], 2) +
            utility.to_hex(populated_data["flag_stop"], 2) +
            utility.to_hex(utility.to_can_unsigned_to_signed(populated_data["angle"])) +
            utility.to_hex(utility.to_can_unsigned_to_signed(populated_data["height_lift"]))
        )
        time.sleep(cls.CAN_SEND_WAIT_TIME_SEC)
        mqtt.send(vehicle_id, "103", can_data)
