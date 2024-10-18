from flask import Flask
from database_prod.api.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_ORIGIN")}})

    app.config.from_object(Config)

    engine = create_engine(app.config['DATABASE_URL'])
    Session = scoped_session(sessionmaker(bind=engine))

    @app.teardown_appcontext
    def remove_session(exception=None):
        Session.remove()

    app.session = Session

    with app.app_context():
        from . import routes

    return app
