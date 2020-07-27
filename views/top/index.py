from flask import Blueprint, current_app

top = Blueprint("top", __name__)


@top.route("/hello")
def echo():
    current_app.logger.debug("top hello")
    return "Hello World!"
