from flask import Flask, jsonify
from config.settings import settings
from routes.home import home
from routes.users import users 
from utils.app_logger import logger

app = Flask(__name__)


app.register_blueprint(home, url_prefix="/")
app.register_blueprint(users, url_prefix="/users")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.PORT)
