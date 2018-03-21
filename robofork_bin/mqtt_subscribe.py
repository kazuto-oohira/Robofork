import signal
import sys, os, json, time, websocket
import paho.mqtt.client as mqtt

# Shell起動, Background起動時もSIGINTをKeyboardInterruptで捕まえる
signal.signal(signal.SIGINT, signal.default_int_handler)

# Web's library Import
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../robofork_app/libs')
import utility

# MQTT QoS
mqtt_sub_qos = 0

# コマンド引数処理
web_socket_server = '127.0.0.1'
mqtt_server = '127.0.0.1'
elastic_server = '127.0.0.1'

if len(sys.argv) == 4:
    web_socket_server = sys.argv[1]
    mqtt_server = sys.argv[1]
    elastic_server = sys.argv[3]


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Robofork/+/toS", qos=mqtt_sub_qos)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))

    # TODO: 本当はElasticSerachに直接投げたい。それからElasticのPUSH系があればそこから通知っぽく
    # RoboforkStatusへ（ひとまず402だけ）
    data = json.loads(msg.payload.decode('ASCII'))
    if data["id"] == "402":
        x = utility.from_can_singed(int(data["data"][0] + data["data"][1], 16)) / 1000
        y = utility.from_can_singed(int(data["data"][2] + data["data"][3], 16)) / 1000
        speed = utility.from_can_singed(int(data["data"][4] + data["data"][5], 16))
        angle = utility.from_can_singed(int(data["data"][6] + data["data"][7], 16)) * 10

        result = {
            "reload": False,
            "vehicles": [
                {
                    "id": "1",
                    "vehicle_status": {
                        "vehicle_operation_plan_id": 1,
                        "status_code": 0,
                        "status_name": "--"
                    },
                    "vehicle_positions": [
                        {
                            "x": x,
                            "y": y,
                            "task": 0,
                            "speed": speed,
                            "angle": angle
                        }
                    ]
                }
            ]
        }
        # print(json.dumps(result, indent=4))

        ws2 = websocket.create_connection("ws://" + web_socket_server + "/vehicle_operation_status")
        ws2.send(json.dumps(result))
        ws2.close()

    # MQTTテストへ
    ws = websocket.create_connection("ws://" + web_socket_server + "/mqtt_test_ws")
    ws.send(msg.payload.decode('ASCII'))
    ws.close()


# MQTT
while True:
    try:
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
        time.sleep(5)
