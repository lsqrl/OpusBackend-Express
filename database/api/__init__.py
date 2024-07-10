from flask import Flask
from .config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

def create_app():
    app = Flask(__name__)
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
