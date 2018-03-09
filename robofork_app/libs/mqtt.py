import json
import paho.mqtt.client as mqtt
from django.conf import settings
from robofork_app.libs import utility


def send(serial_number, can_id, can_data):
    payload_data = {
        'serial_number': serial_number,
        'id': can_id,
        'data': utility.to_can_data(can_data)
    }
    payload_json = json.dumps(payload_data)
    print('MQTT->: ' + payload_json)

    # MQTT送信
    client = mqtt.Client()
    client.connect(settings.MQTT_SERVER['IP'], settings.MQTT_SERVER['PORT'], 60)
    client.publish("Robofork/" + serial_number + "/toR", payload_json)
    client.disconnect()

    return True
