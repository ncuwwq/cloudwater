from flask_restful import Resource, reqparse
import paho.mqtt.client as mqtt
from app.configFiles.emqxConfig import EMQX
from app.emqx.models.task_model import Task as TaskModel
from app import db
import datetime


def to_dict(t):
    status = {0: "未开始", 1: "已完成", 2: "进行中", 3: "已取消"}
    info = {
        "id": str(t.id),
        "startDate": t.startDate,
        "endDate": t.endDate,
        "status": status[t.done],
        "isTouchMove": False,
    }
    return info


class Emqx(Resource):
    def post(self):
        req = reqparse.RequestParser()
        req.add_argument('data', type=dict, required=True, location='json')
        args = req.parse_args()['data']
        if args['type'] == "0":
            try:
                client = mqtt.Client()
                client.connect(EMQX.host, EMQX.port)
                client.publish('switch', payload=args['data'], qos=0)

            except:
                return {
                    "status": 400
                }
        elif args['type'] == "1":
            data = args['data']
            current = datetime.datetime.now()
            current = current.strftime("%m/%d %H:%M")
            startDate = data["startDate"][0:2] + "/" + data["startDate"][3:5] + " " + data["startDate"][7:]
            endDate = data["endDate"][0:2] + "/" + data["endDate"][3:5] + " " + data["endDate"][7:]
            if startDate >= endDate or startDate < current:
                return {
                    "status": 400
                }
            task = TaskModel(startDate=data['startDate'], endDate=data['endDate'], done=0)
            db.session.add(task)
            db.session.flush()
            db.session.commit()
            try:
                client = mqtt.Client()
                client.connect(EMQX.host, EMQX.port)
                timeDate = {"startDate": startDate, "endDate": endDate, "id": task.id}
                client.publish('setTime', payload=str(timeDate), qos=0)
            except:
                return {
                    "status": 400
                }
        return {
            "status": 200
        }

    def get(self):
        tasklist = TaskModel.query.order_by(TaskModel.id.desc()).all()
        if not tasklist:
            return {
                "status": 200,
                "tasklist": []
            }
        info = []
        for t in tasklist:
            info.append(to_dict(t))
        return {
            "status": 200,
            "tasklist": info
        }

    def put(self):
        req = reqparse.RequestParser()
        req.add_argument('data', type=dict, required=True, location='json')
        args = req.parse_args()['data']
        id = args["id"]
        try:
            client = mqtt.Client()
            client.connect(EMQX.host, EMQX.port)
            client.publish('delTask', payload=id, qos=0)
            task = TaskModel.query.filter_by(id=id).first()
            task.done = 3
            db.session.commit()
        except:
            return {
                "status": 400
            }
        return {
            "status": 200
        }
