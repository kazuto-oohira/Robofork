import time, json
from . import can_const
from robofork_app.libs import utility, mqtt
from robofork_app.models.vehicle_operation_plan import VehicleOperationPlan


class RouteOperationService:

    CAN_SEND_WAIT_TIME_SEC = 0.02

    @classmethod
    def execute_route_operation(cls, vehicle_operation_plan_id=-1):

        # ルート情報を取得する（取得不可なら500で落ちる）
        vehicle_operation_plan = VehicleOperationPlan.objects.get(pk=vehicle_operation_plan_id)
        route_operation_json = json.loads(vehicle_operation_plan.route_operation_json)
        if len(route_operation_json) == 0:
            raise ValueError

        # なにもしないタスク(255)は送らない
        edit_route_operation = []
        for row in route_operation_json:
            if row["task"] != can_const.ROUTE_TASK_NOTHING:
                edit_route_operation.append(row)

        # AfterTaskを2行で送信する場合は件数確認
        route_count = len(edit_route_operation)
        for row in edit_route_operation:
            if row["afterTask"] != can_const.ROUTE_TASK_NOTHING:
                route_count += 1

        # TODO: バグ？件数が1件多くなる
        route_count = route_count - 1

        # 件数を取得してPreMap送信
        mqtt.send(vehicle_operation_plan.vehicle_id, can_const.CAN_ID_SND_MAP_PRE_INFO,
                  utility.to_hex(vehicle_operation_plan_id) + utility.to_hex(route_count) + "00000000")

        time.sleep(cls.CAN_SEND_WAIT_TIME_SEC)

        for i in range(2):  # どうにもECUがCANを取りこぼすので2回連続で送る
            index = 1
            for row in edit_route_operation:

                # 初期値設定＆Populate
                data = {
                    "index": index,
                    "x": int(float(row.get("x", 0)) * 1000),
                    "y": int(float(row.get("y", 0)) * 1000),
                    "speed": int(row.get("speed", 1000)),
                    "task": int(row.get("task", 255)),
                    "after_task": int(row.get("afterTask", 255)),
                    "flag_stop": 0,
                    "angle": int(row.get("angle", 0)),
                    "height_lift": int(row.get("liftHeight", 0))
                }

                # 最後の行なら必ずflag_stopをONにする
                if index == len(edit_route_operation):
                    data["flag_stop"] = 1

                # 送信
                cls.__send_route_data(vehicle_operation_plan.vehicle_id, data)

                # AfterTaskが定義されていれば、AfterTaskをTaskに置き換えて再送信
                if data["after_task"] != 255:
                    data["task"] = data["after_task"]
                    cls.__send_route_data(vehicle_operation_plan.vehicle_id, data)

                index += 1

        # 実行開始
        time.sleep(cls.CAN_SEND_WAIT_TIME_SEC)
        mqtt.send(vehicle_operation_plan.vehicle_id, can_const.CAN_ID_SND_ACTION,
                  utility.to_hex(vehicle_operation_plan_id) + utility.to_hex(1, 2) + utility.to_hex(1, 2) + "00000000")

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
        mqtt.send(vehicle_id, can_const.CAN_ID_SND_MAP_INFO_1, can_data)

        # 荷上下げ関係すればflag_stopをON
        if populated_data["task"] == can_const.ROUTE_TASK_LIFTUP \
                or populated_data["task"] == can_const.ROUTE_TASK_LIFTUP_WITH_TURN \
                or populated_data["task"] == can_const.ROUTE_TASK_LIFTDOWN \
                or populated_data["task"] == can_const.ROUTE_TASK_LIFTDOWN_WITH_TURN:
            populated_data["flag_stop"] = 1

        # タスク
        can_data = (
            utility.to_hex(populated_data["index"]) +
            utility.to_hex(populated_data["task"], 2) +
            utility.to_hex(populated_data["flag_stop"], 2) +
            utility.to_hex(utility.to_can_signed(populated_data["angle"])) +
            utility.to_hex(utility.to_can_signed(populated_data["height_lift"]))
        )
        time.sleep(cls.CAN_SEND_WAIT_TIME_SEC)
        mqtt.send(vehicle_id, can_const.CAN_ID_SND_MAP_INFO_2, can_data)
