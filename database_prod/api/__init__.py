from flask import Flask
from database_prod.api.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "https://opusdigital.vercel.app"}})

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
