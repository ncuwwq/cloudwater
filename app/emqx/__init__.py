from flask import Blueprint
from flask_restful import Api
from app.emqx.resources.emqx import Emqx
from app.emqx.resources.switch import Switch

emqx = Blueprint('emqx', __name__)

emqx_api = Api(emqx)

emqx_api.add_resource(Emqx, '/emqx')
emqx_api.add_resource(Switch, '/switch')