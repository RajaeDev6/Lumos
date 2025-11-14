from flask import Blueprint, jsonify

home = Blueprint("home", __name__)

@home.get("/")
def index():
    return jsonify({"message": "This is home route"})
