import paho.mqtt.client as mqtt
import websocket


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Robofork/+/toS")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))

    # 本当はElasticSerachに直接投げたい。それからElasticのPUSH系があればそこから通知っぽく
    ws = websocket.create_connection("ws://127.0.0.1:8000/mqtt_test_ws")
    ws.send(msg.payload.decode('ASCII'))
    ws.close()


# MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.100.149", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
