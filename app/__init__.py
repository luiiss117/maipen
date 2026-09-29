from flask import Flask
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
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
    app.config["SESSION_PERMANENT"]=False
    app.config["SESSION_TYPE"]="filesystem"
    app.config["SESSION_COOKIE_SECURE"]=True 
    app.config["SESSION_COOKIE_HTTPONLY"]=True 
    app.config["SESSION_COOKIE_SAMESITE"]="Lax"    
    csrf = CSRFProtect(app)
    Session(app)
    return app
    

