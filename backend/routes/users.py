
from flask import Blueprint, jsonify

users = Blueprint("users", __name__)


@users.get("/")
def users_index():
    return jsonify({"message": "This is users route"})
