from flask import Flask
import logging
from views.top.index import top
from views.api.v1.index import api_v1

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
# app.config['IS_PRODUCTION'] = True
app.logger.setLevel(logging.DEBUG)
app.register_blueprint(top)
app.register_blueprint(api_v1, url_prefix="/api/v1")

app.logger.debug("main.py name={}".format(__name__))


if __name__ == "__main__":
    app.logger.debug("Start local flask running.")
    app.run(host="0.0.0.0", port=8080, debug=True)
