import signal
import sys, os, json, time, websocket
import paho.mqtt.client as mqtt

# Shell起動, Background起動時もSIGINTをKeyboardInterruptで捕まえる
signal.signal(signal.SIGINT, signal.default_int_handler)

# Web's library Import
# 読み込むPythonファイルのImportがおかしいとエラーになるぞ
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../robofork_app')
from libs import utility
from services import can_const, vehicle_status_service

# MQTT QoS
mqtt_sub_qos = 0

# コマンド引数処理
web_socket_server = '127.0.0.1:8000'
mqtt_server = '127.0.0.1'
elastic_server = '127.0.0.1'

if len(sys.argv) == 4:
    web_socket_server = sys.argv[1]
    mqtt_server = sys.argv[2]
    elastic_server = sys.argv[3]

# WebSocket
web_socket = None
web_socket_test = None

# データを保持するクラス
vehicle_status = vehicle_status_service.VehicleStatusService()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Robofork/+/toS", qos=mqtt_sub_qos)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    global vehicle_status

    # TODO: 本当はElasticSerachに直接投げたい。それからElasticのPUSH系があればそこから通知っぽく
    # VehicleStatusServiceへ設定する
    mqtt_data = json.loads(msg.payload.decode('ASCII'))

    vehicle_id = mqtt_data["serial_number"]
    vehicle_status.set_data(vehicle_id, mqtt_data)
    result_data = vehicle_status.get_vehicle_status(vehicle_id)
    result_data_json = json.dumps(result_data)
    print(result_data_json)

    # ステータス用ソケットへ
    web_socket.send(result_data_json)
    # MQTTテストへ
    web_socket_test.send(msg.payload.decode('ASCII'))


while True:
    try:
        web_socket = websocket.create_connection("ws://" + web_socket_server + "/vehicle_operation_status")
        web_socket_test = websocket.create_connection("ws://" + web_socket_server + "/mqtt_test_ws")

        client = mqtt.Client(protocol=mqtt.MQTTv311)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(mqtt_server, 1883, 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()

    except KeyboardInterrupt:
        # Ctrl+Cは何もせずに終了
        sys.exit()
    except:
        print("MQTT Error:", sys.exc_info()[0])

        # WebSocket Close
        try:
            web_socket.close()
            web_socket_test.close()
        except:
            pass

        time.sleep(2.5)
