from flask import Blueprint, current_app, jsonify, request
import os
from http import HTTPStatus
from consts.response import FORBIDDEN


api_v1 = Blueprint("api_v1", __name__)


@api_v1.route("/environ")
def environ():
    if current_app.config.get("IS_PRODUCTION"):
        return jsonify(FORBIDDEN), HTTPStatus.FORBIDDEN
    values_map = {k: v for k, v in os.environ.items()}
    return jsonify(values_map)


@api_v1.route("/headers")
def headers():
    if current_app.config.get("IS_PRODUCTION"):
        return jsonify(FORBIDDEN), HTTPStatus.FORBIDDEN
    values_map = {k: v for k, v in request.headers.items()}
    return jsonify(values_map)
