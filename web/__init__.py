from flask import Flask
from flask_cors import CORS
def create_app():
    app = Flask(__name__)



    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefic='/')
    app.register_blueprint(auth, url_prefic='/')

    return app