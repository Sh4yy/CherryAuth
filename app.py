from vibora import Vibora
from Routes import bp


def init_db():
    """
    initialize mongodb
    credentials should be in config.json
    :return: True on success
    """
    pass


def create_app():
    """
    initialize the web server
    :return: app on success
    """
    app = Vibora(__name__)
    app.add_blueprint(bp, prefixes={"bp": "/v1"})
    return app
