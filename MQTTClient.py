import paho.mqtt.client as mqtt
from app.configFiles.emqxConfig import EMQX
import threading
import datetime
import requests
import json


def setTime(timeDate, topic):
    while (True):
        current = datetime.datetime.now()
        current = 'b' + "'" + current.strftime("%m/%d %H:%M") + "'"
        if current == str(timeDate):
            client = mqtt.Client()
            client.connect(EMQX.host, EMQX.port)
            if topic == "startDate":
                client.publish('switch', payload="1", qos=0)
            elif topic == "endDate":
                client.publish('switch', payload="0", qos=0)
            break


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == "startDate":
        t = threading.Thread(target=setTime, args=(msg.payload, msg.topic,))
        t.start()
    if msg.topic == "endDate":
        t = threading.Thread(target=setTime, args=(msg.payload, msg.topic,))
        t.start()
    if msg.topic == "update":
        URL = 'http://192.168.1.106:8080/api/emqx/switch'
        headers = {"Content-Type": "application/json"}
        data = json.dumps({"data": {"switch": int(msg.payload)}})
        r = requests.post(URL, headers=headers, data=data)


if __name__ == "__main__":
    client = mqtt.Client("pyClient")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(EMQX.host, EMQX.port, 600)  # 600为keepalive的时间间隔
    client.subscribe([('switch', 0), ('startDate', 0), ('endDate', 0), ('update', 0)])
    client.loop_forever()  # 保持连接
