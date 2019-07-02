from vibora import Vibora
from Routes import bp


app = Vibora(__name__)
app.add_blueprint(bp, prefixes={"bp": "/v1"})


app.run(host="0.0.0.0", port=5001, debug=True)