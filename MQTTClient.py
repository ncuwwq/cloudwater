import paho.mqtt.client as mqtt
from app.configFiles.emqxConfig import EMQX
from sqlalchemy import create_engine
from app.configFiles.sqlConfig import SQLCONFIG
import threading
import datetime
import requests
import json
import inspect
import ctypes

ts = {}
engine = create_engine(SQLCONFIG.SQLALCHEMY_DATABASE_URI)


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def setTime(timeDate, client):
    global engine
    while (True):
        current = datetime.datetime.now()
        current = current.strftime("%m/%d %H:%M")
        if current == timeDate["startDate"]:
            client.publish('switch', payload="1", qos=0)
            engine.execute("update task set done = {0}  where id = {1}".format(2, timeDate["id"]))
            break
    while (True):
        current = datetime.datetime.now()
        current = current.strftime("%m/%d %H:%M")
        if current == timeDate["endDate"]:
            client.publish('switch', payload="0", qos=0)
            del ts[timeDate["id"]]
            engine.execute("update task set done = {0}  where id = {1}".format(1, timeDate["id"]))
            break


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))


def on_message(client, userdata, msg):
    global ts
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == "setTime":
        info = eval(msg.payload)
        t = threading.Thread(target=setTime, name=info["id"], args=(info, client))
        t.start()
        ts[info["id"]] = t
    if msg.topic == "delTask":
        if int(msg.payload) in ts:
            t = ts[int(msg.payload)]
            stop_thread(t)
            del ts[int(msg.payload)]

    if msg.topic == "update":
        URL = 'http://' + EMQX.host + ':8080/api/emqx/switch'
        headers = {"Content-Type": "application/json"}
        data = json.dumps({"data": {"switch": int(msg.payload)}})
        r = requests.post(URL, headers=headers, data=data)


if __name__ == "__main__":
    client = mqtt.Client("pyClient")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(EMQX.host, EMQX.port, 600)  # 600为keepalive的时间间隔
    client.subscribe([('setTime', 0), ('update', 0), ('delTask', 0), ('delRe', 0)])
    client.loop_forever()  # 保持连接
