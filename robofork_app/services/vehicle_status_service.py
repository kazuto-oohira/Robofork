import sys, os, datetime
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

from . import can_const
from robofork_app.libs import utility


class VehicleStatusService:
    PUBLISH_TO_CLIENT_INTERVAL_SEC = 1.5

    def __init__(self):
        self.__vehicle_status_list = {}
        self.__last_publish_to_client = datetime.datetime.now()
        self.__force_send_status_flag = False


    def set_data(self, vehicle_id, data):
        if vehicle_id in self.__vehicle_status_list.keys():
            vehicle_status = self.__vehicle_status_list[vehicle_id]
        else:
            vehicle_status = VehicleStatus(vehicle_id)

        if data["id"] == can_const.CAN_ID_RCV_FORK_STATUS_1:
            self.__set_vehicle_status_1(vehicle_status, data)
        elif data["id"] == can_const.CAN_ID_RCV_FORK_STATUS_2:
            self.__set_vehicle_status_2(vehicle_status, data)
        elif data["id"] == can_const.CAN_ID_RCV_FORK_STATUS_3:
            self.__set_vehicle_status_3(vehicle_status, data)
        elif data["id"] == can_const.CAN_ID_RCV_FORK_ROAD_CELL:
            self.__set_vehicle_road_cell(vehicle_status, data)
        elif data["id"] == can_const.CAN_ID_RCV_FORK_LIFT_HEIGHT:
            self.__set_vehicle_lift_height(vehicle_status, data)
        elif data["id"] == can_const.CAN_ID_RCV_FORK_INTERLOCK_1:
            self.__set_vehicle_interlock_1(vehicle_status, data)
            self.__force_send_status_flag = True
        elif data["id"] == can_const.CAN_ID_RCV_FORK_INTERLOCK_2:
            self.__set_vehicle_interlock_2(vehicle_status, data)
            self.__force_send_status_flag = True
        elif data["id"] == can_const.CAN_ID_RCV_FORK_ARM_SLANT:
            self.__set_vehicle_lift_slant(vehicle_status, data)

        self.__vehicle_status_list[vehicle_id] = vehicle_status


    def get_vehicle_status(self, vehicle_id):
        if vehicle_id in self.__vehicle_status_list.keys():
            vehicle_status = self.__vehicle_status_list[vehicle_id]
        else:
            vehicle_status = VehicleStatus(vehicle_id)
            self.__vehicle_status_list[vehicle_id] = vehicle_status

        return_data = {
            "vehicles": [
                {
                    "id": vehicle_status.vehicle_id,
                    "reload": False,
                    "vehicle_status": {
                        # ID
                        "vehicle_operation_plan_id": vehicle_status.operation_id,

                        # 各ステータスをまとめた情報
                        "vehicle_status": vehicle_status.fork_status,
                        "status_code": vehicle_status.get_status_code(),
                        "status_name": vehicle_status.get_status_name(),

                        # 各ステータス
                        "battery": vehicle_status.battery,
                        "weight_road_cell": vehicle_status.weight_road_cell,
                        "lift_height": vehicle_status.lift_height,
                        "interlock_fork_tip_1": vehicle_status.interlock_fork_tip_1,
                        "interlock_fork_tip_2": vehicle_status.interlock_fork_tip_2,
                        "interlock_fork_tip_3": vehicle_status.interlock_fork_tip_3,
                        "interlock_fork_tip_4": vehicle_status.interlock_fork_tip_4,
                        "interlock_pallet_switch": vehicle_status.interlock_pallet_switch,
                        "interlock_ground_hole_right": vehicle_status.interlock_ground_hole_right,
                        "interlock_ground_hole_left": vehicle_status.interlock_ground_hole_left,
                        "interlock_ground_hole_center": vehicle_status.interlock_ground_hole_center,
                        "interlock_lrf_front": vehicle_status.interlock_lrf_front,
                        "interlock_lrf_rear": vehicle_status.interlock_lrf_rear,
                        "interlock_body_around_tape": vehicle_status.interlock_body_around_tape,
                        "interlock_emergency_button": vehicle_status.interlock_emergency_button,
                        "lift_slant": vehicle_status.lift_slant,
                    },
                    "vehicle_positions": [
                        # 現在位置情報
                        {
                            "x": vehicle_status.x,
                            "y": vehicle_status.y,
                            "task": vehicle_status.operation_task,
                            "task_name": VehicleStatus.get_task_name(vehicle_status.operation_task),
                            "speed": vehicle_status.speed,
                            "angle": vehicle_status.angle,
                            "weight": vehicle_status.weight,
                            "battery": vehicle_status.battery,
                        }
                    ]
                }
            ]
        }

        # 最後にデータをPublishした時刻と現在時刻を比較して、Interval時間を過ぎていなかったらNoneを戻る
        # クライアントへ送信しない。WebSocketの負荷軽減対策
        if not self.__force_send_status_flag and datetime.datetime.now() < \
                (self.__last_publish_to_client + datetime.timedelta(seconds=self.PUBLISH_TO_CLIENT_INTERVAL_SEC)):
            return None
        else:
            self.__last_publish_to_client = datetime.datetime.now()
            self.__force_send_status_flag = False
            return return_data

    def __set_vehicle_status_1(self, vehicle_status, data):
        vehicle_status.operation_id = int(data["data"][0] + data["data"][1], 16)
        vehicle_status.operation_index = int(data["data"][2] + data["data"][3], 16)
        vehicle_status.operation_task = int(data["data"][4], 16)
        vehicle_status.fork_status = int(data["data"][5], 16)


    def __set_vehicle_status_2(self, vehicle_status, data):
        vehicle_status.x = utility.from_can_singed(int(data["data"][0] + data["data"][1], 16)) / 1000
        vehicle_status.y = utility.from_can_singed(int(data["data"][2] + data["data"][3], 16)) / 1000
        vehicle_status.speed = utility.from_can_singed(int(data["data"][4] + data["data"][5], 16))
        vehicle_status.angle = utility.from_can_singed(int(data["data"][6] + data["data"][7], 16)) * 10


    def __set_vehicle_status_3(self, vehicle_status, data):
        vehicle_status.weight = int(data["data"][0] + data["data"][1], 16)
        vehicle_status.battery = utility.from_can_singed(int(data["data"][2] + data["data"][3], 16)) / 10


    def __set_vehicle_road_cell(self, vehicle_status, data):
        value1 = utility.from_can_singed_2(int(data["data"][0] + data["data"][1], 16)) * 0.01
        value2 = utility.from_can_singed_2(int(data["data"][2] + data["data"][3], 16)) * 0.01
        value3 = utility.from_can_singed_2(int(data["data"][4] + data["data"][5], 16)) * 0.01
        value4 = utility.from_can_singed_2(int(data["data"][6] + data["data"][7], 16)) * 0.01
        vehicle_status.weight_road_cell = value1 + value2 + value3 + value4


    def __set_vehicle_lift_height(self, vehicle_status, data):
        vehicle_status.lift_height = utility.from_can_singed_2(int(data["data"][0] + data["data"][1], 16)) * 0.001


    def __set_vehicle_interlock_1(self, vehicle_status, data):
        vehicle_status.interlock_fork_tip_1 = 1 if (int(data["data"][3], 16) & 0b00000001) else 0
        vehicle_status.interlock_fork_tip_2 = 1 if (int(data["data"][3], 16) & 0b00000010) else 0
        vehicle_status.interlock_fork_tip_3 = 1 if (int(data["data"][3], 16) & 0b00000100) else 0
        vehicle_status.interlock_fork_tip_4 = 1 if (int(data["data"][3], 16) & 0b00001000) else 0
        vehicle_status.interlock_pallet_switch = 1 if (int(data["data"][3], 16) & 0b00010000) else 0


    def __set_vehicle_interlock_2(self, vehicle_status, data):
        vehicle_status.interlock_ground_hole_right = 1 if (int(data["data"][0], 16) & 0b00000010) else 0
        vehicle_status.interlock_ground_hole_left = 1 if (int(data["data"][0], 16) & 0b00000100) else 0
        vehicle_status.interlock_ground_hole_center = 1 if (int(data["data"][0], 16) & 0b00001000) else 0
        vehicle_status.interlock_lrf_front = 0 if ((int(data["data"][1], 16) & 0b00000111) == 0b00000111) else 1
        vehicle_status.interlock_lrf_rear  = 0 if ((int(data["data"][1], 16) & 0b01110000) == 0b01110000) else 1
        vehicle_status.interlock_body_around_tape = 1 if (int(data["data"][0], 16) & 0b00000001) else 0
        vehicle_status.interlock_emergency_button = 0 if ((int(data["data"][0], 16) & 0b01110000) == 0b01110000) else 1


    def __set_vehicle_lift_slant(self, vehicle_status, data):
        vehicle_status.lift_slant = utility.from_can_singed_2(int(data["data"][0] + data["data"][1], 16))


class VehicleStatus:
    @classmethod
    def get_task_name(cls, task_code):
        task_name_list = {
            can_const.ROUTE_TASK_FORWARD: "前進",
            can_const.ROUTE_TASK_REVERSE: "バック",
            can_const.ROUTE_TASK_TURN: "旋回（回転）",
            can_const.ROUTE_TASK_LIFTUP: "荷上げ",
            can_const.ROUTE_TASK_LIFTUP_WITH_TURN: "荷上げ(旋回あり)",
            can_const.ROUTE_TASK_LIFTDOWN: "荷下げ",
            can_const.ROUTE_TASK_LIFTDOWN_WITH_TURN: "荷下げ(旋回あり)",
            can_const.ROUTE_TASK_PAUSE: "一時停止",
            can_const.ROUTE_TASK_NOTHING: "-",
        }
        return task_name_list.get(task_code, "----")


    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.operation_id = 0
        self.operation_index = 0
        self.operation_task = 255
        self.fork_status = 0
        self.x = 0
        self.y = 0
        self.speed = 0
        self.angle = 0
        self.weight = 0
        self.weight_road_cell = 0
        self.battery = 0
        self.lift_height = 0
        self.lift_slant = 0
        self.interlock_fork_tip_1 = 0
        self.interlock_fork_tip_2 = 0
        self.interlock_fork_tip_3 = 0
        self.interlock_fork_tip_4 = 0
        self.interlock_pallet_switch = 0
        self.interlock_ground_hole_right = 0
        self.interlock_ground_hole_left = 0
        self.interlock_ground_hole_center = 0
        self.interlock_lrf_front = 0
        self.interlock_lrf_rear = 0
        self.interlock_body_around_tape = 0
        self.interlock_emergency_button = 0


    def get_status_code(self):
        """
        bit1:緊急停止スイッチ
        bit2:遠隔からの緊急停止
        bit3:インターロック
        bit4:LRF検知
        bit5:路面異常
        bit6:荷重異常
        """
        return 2 if (self.fork_status & 0b00111111) != 0 else 0

        """ Interlock信号を直接見る場合
        if self.interlock_fork_tip_1 or self.interlock_fork_tip_2 or self.interlock_fork_tip_3 or self.interlock_fork_tip_4:
            return 2
        # elif self.interlock_pallet_switch:
        #     return 0
        elif self.interlock_ground_hole_right or self.interlock_ground_hole_left or self.interlock_ground_hole_center:
            return 2
        elif self.interlock_lrf_front or self.interlock_lrf_front:
            return 2
        elif self.interlock_body_around_tape:
            return 2
        elif self.interlock_emergency_button:
            return 2
        else:
            return 0
        """


    def get_status_name(self):
        """
        bit1:緊急停止スイッチ
        bit2:遠隔からの緊急停止
        bit3:インターロック
        bit4:LRF検知
        bit5:路面異常
        bit6:荷重異常
        """
        return_strs = []

        if (self.fork_status & 0b00000001) != 0:
            return_strs.append("緊急停止ボタン")
        elif (self.fork_status & 0b00000010) != 0:
            return_strs.append("遠隔停止")
        elif (self.fork_status & 0b00000100) != 0:
            return_strs.append("インターロック信号検知")
        elif (self.fork_status & 0b00001000) != 0:
            return_strs.append("LRF検知")
        elif (self.fork_status & 0b00010000) != 0:
            return_strs.append("路面異常")
        elif (self.fork_status & 0b00100000) != 0:
            return_strs.append("荷重異常")
        else:
            return VehicleStatus.get_task_name(self.operation_task)

        return "/".join(return_strs)

        """ Interlock信号を直接見る場合
        if self.interlock_emergency_button:
            return "緊急停止ボタン押下"
        elif self.interlock_body_around_tape:
            return "障害物検知(テープスイッチ)"
        elif self.interlock_lrf_front or self.interlock_lrf_front:
            return "障害物検知(LRF)"
        elif self.interlock_ground_hole_right or self.interlock_ground_hole_left or self.interlock_ground_hole_center:
            return "路面異常検知"
        elif self.interlock_fork_tip_1 or self.interlock_fork_tip_2 or self.interlock_fork_tip_3 or self.interlock_fork_tip_4:
            return "爪先光電管接触検知"
        # elif self.interlock_pallet_switch:
        #     return "パレットリミットスイッチ"
        else:
            return VehicleStatus.get_task_name(self.operation_task)
        """