from sanic import Sanic
from routes import bp
from models import *


def create_db():
    """
    initialize and create db models
    :return: True on success
    """
    db.create_tables([User, Session, Credentials])
    return True


def create_app():
    """
    initialize the web server
    :return: app on success
    """
    app = Sanic(__name__)
    app.blueprint(bp, url_prefix="/v1")
    return app


def create_secret():
    """
    create jwt secret if doesnt exist
    :return: True if created
    """

    try:
        JWT.gen_secret()
    except Exception:
        return False

    return True
