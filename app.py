from vibora import Vibora
from Routes import bp
from Utils import config, JWT
from mongoengine import connect


def init_db():
    """
    initialize mongodb
    credentials should be in config.json
    :return: True on success
    """
    connect(config['database']['name'],
            host=config['database']['url'])
    return True


def create_app():
    """
    initialize the web server
    :return: app on success
    """
    app = Vibora(__name__)
    app.add_blueprint(bp, prefixes={"bp": "/v1"})
    return app


def create_secret():
    """
    create jwt secret if doesnt exist
    :return: True if created
    """

    try:
        JWT.gen_secret()
        return True
    except Exception:
        return False
