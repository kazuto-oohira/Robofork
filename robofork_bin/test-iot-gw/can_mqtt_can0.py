#/usr/bin/python
# -*- codint: utf-8 -*-
"""
IoT-GWのcan_mqtt_slcan0.pyのロジックをテストするため
"""

import sys, json, multiprocessing, csv, time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# MQTT QoS
mqtt_pub_qos = 0
mqtt_sub_qos = 1

# Robofork Serial Number
SerialNumber = "1"

# 処理対象の受信CAN-IDリスト
can_id_list = ["401", "402", "403", "27F"]
# 間引かない受信CAN-IDリスト
always_send_can_id_list = ["27F"]

# MQTT
IP = "192.168.1.126"
topic_toR = "Robofork/" + SerialNumber + "/toR"  # From Server to Robofork
topic_toS = "Robofork/" + SerialNumber + "/toS"  # From Robofork to Server

# 過剰送信を防ぐために、同じCAN-ID/Dataは間引く。その判定用の保存データ。
saved_sent_can_data = {}

class CanMessage:
    arbitration_id = -1
    data = []


def can_recv():
    while True:
        bus = []
        with open("test_can_data.csv") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                msg = CanMessage()

                # HEXのテストデータを数値に戻す（以下のロジックはCAN−BUSから取得した数値データだから）
                # MQTT->と同じロジックでやってるから大丈夫でしょ。テストになるでしょ。
                msg.arbitration_id = int(row[0], 16)
                msg.data = [
                    int(row[1], 16),
                    int(row[2], 16),
                    int(row[3], 16),
                    int(row[4], 16),
                    int(row[5], 16),
                    int(row[6], 16),
                    int(row[7], 16),
                    int(row[8], 16),
                ]

                bus.append(msg)

        # ▽▽▽▽ このロジックは本番と同一に合わせること ▽▽▽▽
        for msg in bus:
            can_id = (hex(msg.arbitration_id)[2:]).upper()  # "0x"を外してる
            # print("Can Recv : " + str(can_id) + " " + str(msg))

            # 処理対象のCAN-ID以外は無視
            if can_id not in can_id_list:
                continue

            can_data = list(map(hex, msg.data))
            for i in range(len(can_data)):
                can_data[i] = can_data[i][2:]
                if len(can_data[i]) == 1:
                    can_data[i] = "0" + can_data[i]

            data_mqtt = {"serial_number": SerialNumber, "id": can_id, "data": can_data}
            data_mqtt_json = json.dumps(data_mqtt)

            # 前回同じデータを送っていたら送らない
            if can_id not in always_send_can_id_list:
                if can_id in saved_sent_can_data and saved_sent_can_data[can_id] == can_data:
                    continue

            try:
                mqtt_pub(topic_toS, data_mqtt_json)
                saved_sent_can_data[can_id] = can_data  # 送信データ保存
            except:
                print("MQTT Error :Publish ", sys.exc_info()[0])
                print("id:" + str(can_id) + ", data:" + str(can_data))

        # △△△△ このロジックは本番と同一に合わせること △△△△
            time.sleep(0.5)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def mqtt_pub(topic, data):
    publish.single(topic, data, hostname=IP, qos=mqtt_pub_qos)
    print("Pub : " + data)


def mqtt_sub():
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(topic_toR, qos=mqtt_sub_qos)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        # print(msg.topic+" "+str(msg.payload))
        data = msg.payload.decode('UTF-8')
        data_json = json.loads(data)
        can_id = int(data_json["id"], 16)
        can_data = data_json["data"]
        for i in range(len(can_data)):
            can_data[i] = int(can_data[i], 16)

        print("Sub[HEX]    : " + data_json["id"] + " " + json.dumps(data_json["data"]))
        print("Sub[DECIMAL]: " + str(can_id) + " " + str(can_data))

    try:
        client = mqtt.Client(protocol=mqtt.MQTTv311)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(IP, 1883, 60)
        client.loop_forever()
    except:
        print("MQTT Error :Subscribe ", sys.exc_info()[0])


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if __name__ == "__main__":
    proc_mqtt = multiprocessing.Process(target=mqtt_sub)
    proc_can = multiprocessing.Process(target=can_recv)
    proc_mqtt.start()
    proc_can.start()
