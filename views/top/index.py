from flask import Blueprint, current_app, render_template

top = Blueprint("top", __name__)


@top.route("/hello")
def echo():
    current_app.logger.debug("top hello")
    return render_template("hello.html", title="Hello Today!")
