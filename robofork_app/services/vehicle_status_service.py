import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../robofork_app')

from . import can_const
from libs import utility


class VehicleStatusService:
    def __init__(self):
        self.__vehicle_status_list = {}


    def set_data(self, vehicle_id, data):
        if vehicle_id in self.__vehicle_status_list.keys():
            vehicle_status = self.__vehicle_status_list[vehicle_id]
        else:
            vehicle_status = VehicleStatus(vehicle_id)
            self.__vehicle_status_list[vehicle_id] = vehicle_status

        if data["id"] == can_const.CAN_ID_FORK_STATUS_1:
            self.__set_vehicle_status_1(vehicle_status, data)
        elif data["id"] == can_const.CAN_ID_FORK_STATUS_2:
            self.__set_vehicle_status_2(vehicle_status, data)
        elif data["id"] == can_const.CAN_ID_FORK_STATUS_3:
            pass
        elif data["id"] == can_const.CAN_ID_FORK_ROAD_CELL:
            pass
        elif data["id"] == can_const.CAN_ID_FORK_LIFT_HEIGHT:
            pass
        elif data["id"] == can_const.CAN_ID_FORK_INTERLOCK_1:
            pass
        elif data["id"] == can_const.CAN_ID_FORK_INTERLOCK_2:
            pass
        elif data["id"] == can_const.CAN_ID_FORK_ARM_SLANT:
            pass


    def get_vehicle_status(self, vehicle_id):
        if vehicle_id in self.__vehicle_status_list.keys():
            vehicle_status = self.__vehicle_status_list[vehicle_id]
        else:
            vehicle_status = VehicleStatus(vehicle_id)
            self.__vehicle_status_list[vehicle_id] = vehicle_status

        return {
            "reload": False,
            "vehicles": [
                {
                    "id": vehicle_status.vehicle_id,
                    "vehicle_status": {
                        "vehicle_operation_plan_id": vehicle_status.operation_id,
                        "status_code": vehicle_status.get_status_code(),
                        "status_name": vehicle_status.get_status_name(),
                    },
                    "vehicle_positions": [
                        {
                            "x": vehicle_status.x,
                            "y": vehicle_status.y,
                            "task": vehicle_status.operation_task,
                            "task_name": VehicleStatus.get_task_name(vehicle_status.operation_task),
                            "speed": vehicle_status.speed,
                            "angle": vehicle_status.angle,
                        }
                    ]
                }
            ]
        }


    def __set_vehicle_status_1(self, vehicle_status, data):
        vehicle_status.operation_id = int(data["data"][0] + data["data"][1], 16)
        vehicle_status.operation_index = int(data["data"][2] + data["data"][3], 16)
        vehicle_status.operation_task = int(data["data"][4], 16)
        vehicle_status.operation_status = int(data["data"][5], 16)


    def __set_vehicle_status_2(self, vehicle_status, data):
        vehicle_status.x = utility.from_can_singed(int(data["data"][0] + data["data"][1], 16)) / 1000
        vehicle_status.y = utility.from_can_singed(int(data["data"][2] + data["data"][3], 16)) / 1000
        vehicle_status.speed = utility.from_can_singed(int(data["data"][4] + data["data"][5], 16))
        vehicle_status.angle = utility.from_can_singed(int(data["data"][6] + data["data"][7], 16)) * 10


class VehicleStatus:
    TASK_FORWARD = 0
    TASK_REVERSE = 1
    TASK_TURN = 2
    TASK_LIFTUP = 3
    TASK_LIFTUP_WITH_TURN = 4
    TASK_LIFTDOWN = 5
    TASK_LIFTDOWN_WITH_TURN = 6
    TASK_PAUSE = 7
    TASK_NOTHING = 255


    @classmethod
    def get_task_name(cls, task_code):
        task_name_list = {
            cls.TASK_FORWARD: "前進",
            cls.TASK_REVERSE: "バック",
            cls.TASK_TURN: "旋回（回転）",
            cls.TASK_LIFTUP: "荷上げ",
            cls.TASK_LIFTUP_WITH_TURN: "荷上げ(旋回あり)",
            cls.TASK_LIFTDOWN: "荷下げ",
            cls.TASK_LIFTDOWN_WITH_TURN: "荷下げ(旋回あり)",
            cls.TASK_PAUSE: "一時停止",
            cls.TASK_NOTHING: "-",
        }
        return task_name_list.get(task_code, "----")


    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.operation_id = 0
        self.operation_index = 0
        self.operation_task = 255
        self.operation_status = 0
        self.x = 0
        self.y = 0
        self.speed = 0
        self.angle = 0


    def get_status_code(self):
        return 0


    def get_status_name(self):
        return VehicleStatus.get_task_name(self.operation_task)
