import sys, os, datetime
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

from . import can_const
from robofork_app.libs import utility, mqtt
from robofork_app.models import Vehicle

class PlcService:
    def __init__(self):
        pass


    def receive_plc_message(self, data):
        # 存在する全車両に緊急指示を投げる
        vehicles = Vehicle.get_list(location_id=1)  # ひとまず1固定
        for vehicle in vehicles:
            mqtt.send(vehicle.id, can_const.CAN_ID_SND_EMERGENCY, "0100000000000000")
