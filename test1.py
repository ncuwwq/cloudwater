import paho.mqtt.client as mqtt
from app.configFiles.emqxConfig import EMQX


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(EMQX.host, 1883)  # 600为keepalive的时间间隔
    client.publish('switch', payload="0", qos=0)
