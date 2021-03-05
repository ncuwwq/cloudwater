from flask_restful import Resource, reqparse
import paho.mqtt.client as mqtt
from app.configFiles.emqxConfig import EMQX
from app.emqx.models.switch_model import Switch as SwitchModel
from app import db


class Switch(Resource):
    def post(self):
        req = reqparse.RequestParser()
        req.add_argument('data', type=dict, required=True, location='json')
        data = req.parse_args()['data']
        try:
            switch = SwitchModel.query.filter_by(id=1).first()
            switch.status = data['switch']
            db.session.commit()
        except:
            return {
                "status": 400
            }
        return {
            "status": 200
        }

    def get(self):
        switch = SwitchModel.query.filter_by(id=1).first()
        return {
            "status": 200,
            "switch": switch.status
        }
