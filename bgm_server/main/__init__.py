import os
import flask
from flask_redis import FlaskRedis
from config import CONFIG_BY_NAME

redis_client = FlaskRedis()


def create_app():
    app = flask.Flask(__name__)
    app.config.from_object(CONFIG_BY_NAME[os.getenv('ENVIRONMENT', 'dev')])
    print "--- Environment %s initialized ---" % (app.config['ENVIRONMENT'])
    redis_client.init_app(app)

    from main.flaskutils import bp
    app.register_blueprint(bp)
    app.app_context().push()

    return app
