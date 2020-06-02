from flask import Blueprint
from flask_restplus import Api

bp = Blueprint('api', __name__)
API = Api(bp, version='0.1', title='BoardGameMate API', description='', validate=True)

import main.flaskutils.kingdominocontroller
