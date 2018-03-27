from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from robofork_app.libs import mqtt, utility
from robofork_app.services import can_const


@csrf_exempt
def auto_control_flag(request, vehicle_id=0):
    set_auto_flag = int(request.POST.get('set_auto_flag', 0))

    # データ作成して送信
    send_data = utility.to_hex(0, 4) + utility.to_hex(set_auto_flag, 2) + utility.to_hex(0, 10)
    mqtt.send(vehicle_id, can_const.CAN_ID_SND_ACTION, send_data)

    return JsonResponse({ "result": True })


@csrf_exempt
def manual_control(request, vehicle_id=0):
    # 本当はvehicle_idでDB検索して存在しなければ404出したほうがいいんだけど、
    # 手動操作っていう性質上パフォーマンスを重視したいのでやってない。
    speed = int(request.POST.get('speed', 0))
    stair_angle = int(request.POST.get('stair_angle', 0))
    fork_up = int(request.POST.get('fork_up', 0))
    tilt_up = int(request.POST.get('tilt_up', 0))
    print(request.POST)

    fork_up_value = -999
    if fork_up == 1:
        fork_up_value = 999
    elif fork_up == -1:
        fork_up_value = 0

    tilt_up_value = 0
    if tilt_up == 1:
        tilt_up_value = 2
    elif tilt_up == -1:
        tilt_up_value = 4

    # データ作成して送信
    send_data = utility.to_hex(0, 2) + \
                utility.to_hex(utility.to_can_signed(speed), 4) + \
                utility.to_hex(utility.to_can_signed(stair_angle), 4) + \
                utility.to_hex(utility.to_can_signed(fork_up_value), 4) + \
                utility.to_hex(tilt_up_value, 2)
    mqtt.send(vehicle_id, can_const.CAN_ID_SND_MANUAL_CTRL, send_data, qos=mqtt.MQTT_QOS_NORMAL)

    return JsonResponse({ "result": True })


@csrf_exempt
def operation_flag(request, vehicle_id=0):
    emergency_flag = int(request.POST.get('emergency_flag', 0))
    demo_obstacle_flag_1 = int(request.POST.get('demo_obstacle_flag_1', 0))
    demo_obstacle_flag_2 = int(request.POST.get('demo_obstacle_flag_2', 0))

    # データ作成して送信
    send_data = \
        utility.to_hex(emergency_flag, 2) + \
        utility.to_hex(demo_obstacle_flag_1, 2) + \
        utility.to_hex(demo_obstacle_flag_2, 2) + \
        utility.to_hex(0, 10)

    mqtt.send(vehicle_id, can_const.CAN_ID_SND_EMERGENCY, send_data)

    return JsonResponse({ "result": True })
