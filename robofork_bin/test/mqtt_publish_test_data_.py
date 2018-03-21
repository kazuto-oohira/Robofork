"""
MQTTへ送られるデータを模擬する
"""
import sys, csv, time, datetime
import paho.mqtt.client as mqtt_client

# Shell起動, Background起動時もSIGINTをKeyboardInterruptで捕まえる
import signal
signal.signal(signal.SIGINT, signal.default_int_handler)

# MQTT QoS
mqtt_pub_qos = 0

# コマンド引数処理
mqtt_server = '192.168.13.27'
test_data_file = '/Users/sngmr/Projects/NKC/RoboFork/sources/RoboforkWeb/robofork_bin/test/test_data/can-all-mqtt-log.txt'
if len(sys.argv) == 3:
    mqtt_server = sys.argv[1]
    test_data_file = sys.argv[2]


def publish_test_data():
    try:
        while True:
            client = mqtt_client.Client(protocol=mqtt_client.MQTTv311)
            client.connect(mqtt_server, keepalive=60)

            with open(test_data_file) as f:
                reader = csv.reader(f, delimiter="#")
                for row in reader:
                    client.publish(row[0], row[1])

                    print(str(datetime.datetime.now()) + " " + row[0] + "#" + row[1])
                    time.sleep(0.05)

    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    publish_test_data()
