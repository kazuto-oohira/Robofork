import json
import paho.mqtt.client as mqtt
from django.conf import settings
from robofork_app.libs import utility

# MQTT QoS
MQTT_QOS_NORMAL = 0
MQTT_QOS_GOOD = 1


def send(serial_number, can_id, can_data, qos=MQTT_QOS_GOOD):
    """
    MQTTへ送信する
    :param serial_number: フォーク識別No
    :param can_id: CAN-ID(HEX形式)
    :param can_data: (HEX形式)
    :param qos: QoS(0-1) 2はなぜか動かない
    :return:
    """
    payload_data = {
        'serial_number': serial_number,
        'id': can_id,
        'data': utility.to_can_data(can_data)
    }
    payload_json = json.dumps(payload_data)
    print('MQTT->: ' + payload_json)

    # MQTT送信
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect(settings.MQTT_SERVER['IP'], settings.MQTT_SERVER['PORT'], 60)
    client.publish("Robofork/" + serial_number + "/toR", payload=payload_json, qos=qos)
    client.disconnect()

    return True
