from flask_restful import Resource, reqparse
import paho.mqtt.client as mqtt
from app.configFiles.emqxConfig import EMQX
from app.emqx.models.task_model import Task as TaskModel
from app import db
import datetime


def to_dict(t):
    info = {
        "id": t.id,
        "startDate": t.startDate,
        "endDate": t.endDate
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
            db.session.commit()
            try:
                client = mqtt.Client()
                client.connect(EMQX.host, EMQX.port)
                client.publish('startDate', payload=startDate, qos=0)
                client.publish('endDate', payload=endDate, qos=0)
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
                "status": 0
            }
        info = []
        for t in tasklist:
            info.append(to_dict(t))
        return {
            "status": 200,
            "tasklist": info
        }
