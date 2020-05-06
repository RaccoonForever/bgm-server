# pylint: disable=line-too-long
"""
Main script to run the server
"""

import os
import flask
from flask import Blueprint
from flask_restplus import Api
from config import CONFIG_BY_NAME
from main.flaskutils.kingdominocontroller import API as KINGDOMINO_NS
from main.yolov3.yolomodels import load_models

BLUEPRINT = Blueprint('api', __name__)

# initialize our Flask application
APP = flask.Flask(__name__)
APP.config.from_object(CONFIG_BY_NAME[os.getenv('ENVIRONMENT', 'dev')])
print "--- Environment %s initialized ---" % (APP.config['ENVIRONMENT'])

API = Api(BLUEPRINT, version='0.1', title='BoardGameMate API', description='', validate=True)
API.add_namespace(KINGDOMINO_NS, path='/kingdomino')

APP.register_blueprint(BLUEPRINT)
APP.app_context().push()


if __name__ == "__main__":
    print "* Loading TF models and Flask starting server... \n please wait until server has fully started *"
    load_models()
    APP.run(host=APP.config['FLASK_RUN_HOST'], port=APP.config['FLASK_RUN_PORT'])
