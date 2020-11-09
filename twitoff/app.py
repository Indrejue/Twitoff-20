"""Main app file for Twitoff"""

from flask import Flask, render_template
from .models import DB, User


def create_app():
    """Creating and configuring an instance of the Flask app"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title="home", users=User.query.all())

    return app
