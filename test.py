import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))



if __name__ == "__main__":
    client = mqtt.Client("pyClient")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('192.168.137.130', 1883, 600)  # 600为keepalive的时间间隔
    client.subscribe('switch', qos=0)
    client.loop_forever()  # 保持连接

