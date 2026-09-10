from flask import Flask
from flask_session import Session
from os import environ
from dotenv import load_dotenv
from app.routes import blueprints
import app.database


def create_app():
    database.init_db()
    app = Flask(__name__)
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    load_dotenv()
    app.secret_key = environ["SECRET_KEY"] # Secret key for Session
    app.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
    app.config["SESSION_TYPE"] = "filesystem"     # Store session data in files
    Session(app)
    return app


if __name__ == '__main__':
    database.init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
    

